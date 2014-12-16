#include <stdio.h>
#include <mem.h>
#include <malloc.h>
#include <conio.h>
#include "slots.h"
#include "packets.h"
#include "movie.h"
#include "storage.h"
#include "map.h"
#include "checkalloc.h"

#include <dos.h> // For FP_*
#define FP_L(p) (((int32)(FP_SEG(p)) << 4) + FP_OFF(p))

#define SLOTS 40

#define MAX_OPLOG 8000
#define MAX_PATH 64
#define MAX_IDS 100
#define MAX_MAP 2000

const int port = 16742;

JPStorage *storage;

JPSlot *slots;

point *path_buffer;

JPHeading *oplog_buffer;

point *map_chunk;

JPID *ids_buffer;

void respond_error(JPSlot *slot, int code)
{
	*(int *)slot->buffer = code;
   slot->data_length = 0;
}

void process_request(JPSlot *slot)
{
	JPRequest *request = (JPRequest *)slot->buffer;
   int ret, count, bytes;
   switch (request->type)
   {
   case REQ_Put:
		jp_clear_path(path_buffer, MAX_PATH);
		ret = jp_build_path(request->source, request->destination, path_buffer, map_chunk);
      if (ret)
      	respond_error(slot, ret);
		else
      {
      	jp_store_path(storage, *(JPHeading *)&request->source, request->id);
      	bytes = jp_get_bytes(path_buffer, slot->buffer, 2, SLOT_BUFFER - 2);
         *(int *)slot->buffer = 0;
         slot->data_length = bytes + 2;
      }
   	break;
   case REQ_Get:
		count = jp_load_ids(storage, *(JPHeading *)&request->source, ids_buffer, MAX_IDS);
      _fmemcpy(slot->buffer + 2, ids_buffer, SLOT_BUFFER - 2);
      *(uint16 *)slot->buffer = count;
      slot->data_length = count * sizeof(JPID) + 2;
   	break;
   default:
   	slot->data_length = 0;
   }
   slot->position = 0;
}

void init_slot(JPSlot *slot)
{
	slot->state = SLOT_Listen;
	slot->position = 0;
	slot->data_length = 0;
	tcp_listen(&slot->socket, port, 0, 0, NULL, 0);
}

void tick_slot(JPSlot *slot, int id)
{
	if (!tcp_tick((sock_type *)&slot->socket))
   {
     	printf("!tcp_tick\n");
     	init_slot(slot);
      return;
   }
	switch (slot->state)
   {
   case SLOT_Listen:
   	if (tcp_established(&slot->socket))
      {
      	printf("Accepted client in slot %d!\n", id);
         slot->state = SLOT_Receive;
      }
      break;
   case SLOT_Receive:
   	jp_slot_read(slot);
      if (slot->position >= sizeof(JPRequest))
      {
       	process_request(slot);
         slot->state = SLOT_Send;
      }
      break;
   case SLOT_Send:
   	jp_slot_write(slot);
      if (slot->position >= slot->data_length)
      	init_slot(slot);
   }
}

bool poll() // TODO: free sockets by timeout
{
	if (kbhit() && getch() == 27)
      return false;
	static const char wait[] = "-\|/";
   int i = 0;
   for (JPSlot *slot = slots; slot->next; slot = slot->next)
   {
   	printf("%c\r", wait[i++ % 4]);
   	tick_slot(slot, i);
   }
   return true;
}

void allocate_slots()
{
	JPSlot *slot;
	slots = slot = (JPSlot *)checkalloc(sizeof(JPSlot));

   for (int i = 1; i < SLOTS; i++)
   {
   	slot->next = (JPSlot *)checkalloc(sizeof(JPSlot));
      slot = slot->next;
      printf("Allocated %d slots...\n", i + 1);
      printf("Last slot is at %p (%ld).\n", slot, FP_L(slot));
   }
   slot->next = NULL;
   int32 size = FP_L(slot) + sizeof(JPSlot) - FP_L(slots);
   int32 opt_size = (int32)sizeof(JPSlot) * SLOTS;
   printf("All slots occupy %ld bytes (%ld%% of optimal).\n", size, 100 * size / opt_size);
}

void allocate_memory() //TODO use checkmallocs in storage code
{
	printf("Slot size is %d bytes.\n", sizeof(JPSlot));
	allocate_slots();
   path_buffer = (point *)checkalloc(sizeof(point) * MAX_PATH);
   oplog_buffer = (JPHeading *)checkalloc(sizeof(JPHeading) * MAX_OPLOG);
   map_chunk = (point *)checkalloc(sizeof(point) * MAX_MAP);
   ids_buffer = (JPID *)checkalloc(sizeof(JPID) * MAX_IDS);
	storage = jp_storage_init("store", oplog_buffer, MAX_OPLOG);
	jp_init_map("map");
	printf("Memory allocated.\n");
}

void cleanup()
{
	jp_storage_free(storage);
}

void main()
{
	printf("Server started.\n");
   sock_init();
	allocate_memory();
   int count = 0;
	for (JPSlot *slot = slots; slot->next; slot = slot->next)
   {
   	init_slot(slot);
      printf("Initialized %d slots...\n", ++count);
   }
   while (poll()) ;
   cleanup();
   printf("Exiting server...");
}
