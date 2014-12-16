#include <conio.h>
#include <stdio.h>
#include <mem.h>
#include <dos.h>
#include "types.h"
#include "checkalloc.h"

#include <stdlib.h>
#include <dir.h>
#include <zlib.h>

#define VIDEO_INT           0x10
#define SET_MODE            0x00
#define VGA_256_COLOR_MODE  0x13
#define TEXT_MODE           0x03

#define SCREEN_WIDTH        320
#define SCREEN_HEIGHT       200

#define PALETTE_INDEX       0x03c8
#define PALETTE_DATA        0x03c9

byte *VGA = (byte *)0xA0000000L;
uint16 *my_clock = (uint16 *)0x0000046C;

#define JP_FRAME_DATA_SIZE 64000U
#define JP_FRAME_PAL_SIZE 768

#define CHUNK 0x4000

#define windowBits 15
#define ENABLE_ZLIB_GZIP 32

struct JPImageFrame
{
	byte palette[JP_FRAME_PAL_SIZE];
	void *data;
};

struct JPImageStream
{
	byte *in_buffer;
   byte *out_buffer;
   size_t ready;
   size_t position;
   FILE *file;
   z_stream zstr;
};

void set_mode(byte mode)
{
	union REGS regs;

   regs.h.ah = SET_MODE;
  	regs.h.al = mode;
  	int86(VIDEO_INT, &regs, &regs);
}

void show_frame(JPImageFrame *frame)
{
	outp(PALETTE_INDEX, 0);
  	for (int i = 0; i < JP_FRAME_PAL_SIZE; i++)
		outp(PALETTE_DATA, frame->palette[i]);

   _fmemcpy(VGA, frame->data, JP_FRAME_DATA_SIZE);
}

JPImageStream *jp_stream_open(const char *path)
{
	JPImageStream *stream = (JPImageStream *)checkalloc(sizeof(JPImageStream)); //TODO All mallocs to safe
   stream->ready = stream->position = 0;
	stream->file = fopen(path, "rb");
   if (!stream->file)
	{
   	printf("Failed to open file.\n");
      _ffree(stream);
		return NULL;
   }
	stream->in_buffer = (byte *)checkalloc(CHUNK);
	stream->out_buffer = (byte *)checkalloc(CHUNK);
   _fmemset(&stream->zstr, 0, sizeof(z_stream));
	stream->zstr.zalloc = Z_NULL;
   stream->zstr.zfree = Z_NULL;
   stream->zstr.opaque = Z_NULL;
   stream->zstr.next_in = stream->in_buffer;
   stream->zstr.avail_in = 0;
   stream->zstr.next_out = stream->out_buffer;
   int result = inflateInit2(&stream->zstr, windowBits | ENABLE_ZLIB_GZIP);
   if (result < 0)
   {
   	printf("inflateInit2 returned error %d.\n", result);
		//TODO free it all
      return NULL;
   }
   return stream;
}

void jp_stream_close(JPImageStream *stream)
{
	_ffree(stream->in_buffer);
	_ffree(stream->out_buffer);
   inflateEnd(&stream->zstr);
   fclose(stream->file);
	_ffree(stream);
}

size_t jp_stream_read(JPImageStream *stream, void *buffer, size_t length)
{
	//printf("starting to read %u bytes\n", length);getch();
	size_t to_read = length;
	while (to_read)
   {
   	//printf("entering new iteration\n");getch();
		if (stream->ready)
   	{
   		//printf("ready: %u bytes\n", stream->ready);getch();
   		size_t to_take = min(to_read, stream->ready);
   		//printf("will take %u bytes\n", to_take);getch();
      	_fmemcpy(buffer, stream->out_buffer + stream->position, to_take);
      	to_read -= to_take;
      	buffer = (byte *)buffer + to_take;
      	stream->ready -= to_take;
         stream->position += to_take;
   	}
      if (to_read == 0)
      	break;
   	//printf("trying to inflate more\n");getch();
      stream->zstr.next_out = stream->out_buffer;
   	stream->zstr.avail_out = CHUNK;
      //printf("zstr state: next_in = %p, avail_in = %u, next_out = %p, avail_out = %u\n", stream->zstr.next_in, stream->zstr.avail_in, stream->zstr.next_out, stream->zstr.avail_out);
      inflate(&stream->zstr, Z_NO_FLUSH);
      stream->position = 0;
		if (stream->zstr.avail_out == CHUNK)
      {
   		//printf("failed: avail_out is %u\n", stream->zstr.avail_out);getch();
      	if (feof(stream->file))
         	return length - to_read;
         //printf("it wasn't eof, reading more\n");getch();
         size_t bytes_read = fread(stream->in_buffer, 1, CHUNK, stream->file);
         //printf("read %u bytes\n", bytes_read);getch();
         stream->zstr.next_in = stream->in_buffer;
      	stream->zstr.avail_in = bytes_read;
         stream->zstr.next_out = stream->out_buffer;
         stream->zstr.avail_out = CHUNK;
         //printf("zstr state: next_in = %p, avail_in = %u, next_out = %p, avail_out = %u\n", stream->zstr.next_in, stream->zstr.avail_in, stream->zstr.next_out, stream->zstr.avail_out);
         inflate(&stream->zstr, Z_NO_FLUSH);
         //printf("trying again to inflate more\n");getch();
      }
      /*printf("expecting avail_out = 0, actual is %u\n", stream->zstr.avail_out);getch();
      if (stream->zstr.avail_out)
      {
      	printf("inflate failed unexpectedly.\n");
         return length - to_read;
      }*/
      stream->ready = CHUNK - stream->zstr.avail_out;
   }
   return length;
}

void show_movie(const char *path)
{
	//printf("show_movie entered\n");getch();

	JPImageStream *stream = jp_stream_open(path);
   if (!stream)
   {
   	printf("Failed to open stream.\n");
      return;
   }

   //printf("stream opened\n");getch();

	JPImageFrame frame;
   frame.data = checkalloc(JP_FRAME_DATA_SIZE); //TODO Make safemalloc

   if (!frame.data)
   {
   	printf("Failed to allocate %u bytes.\n", JP_FRAME_DATA_SIZE);
		jp_stream_close(stream);
      return;
   }

   //printf("frame allocated\n");getch();

   set_mode(VGA_256_COLOR_MODE);

   uint16 last_time = *my_clock;
   while (*my_clock == last_time);
   last_time = *my_clock;
   while (true)
   {
   	size_t bytes_read = jp_stream_read(stream, frame.palette, JP_FRAME_PAL_SIZE);
      if (!bytes_read)
      	break;
      jp_stream_read(stream, frame.data, JP_FRAME_DATA_SIZE);
      
      show_frame(&frame);

   	while (*my_clock == last_time);
   	last_time = *my_clock;
   }

	set_mode(TEXT_MODE);

   _ffree(frame.data);
   jp_stream_close(stream);
}

int main()
{
	ffblk entry;

   if (findfirst("*.mov", &entry, 0) == 0)
   {
   	do
      {
      	printf("%s\n", entry.ff_name);
         getch();
         show_movie(entry.ff_name);
      }
      while (findnext(&entry) == 0);
   }
   return 0;
}