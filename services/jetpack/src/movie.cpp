#include <graphics.h>
#include <conio.h>
#include <stdio.h>
#include <malloc.h>
#include <mem.h>
#include "movie.h"
#include "types.h"

#define MAX_IMAGE (int16)(10 * 1024)

int show_movie(const char *path) { }

int show_image(const char *path)
{
	FILE *image = fopen(path, "w");
   if (!image)
   {
   	printf("Failed to open image file.\n");
   	return -1;
   }
	byte *data = (byte *)checkalloc(MAX_IMAGE);
   if (!data)
   {
   	printf("Failed to allocate %d bytes.\n", MAX_IMAGE);
   	return -1;
   }
	_fmemset(data, '@', MAX_IMAGE);

   int gdriver = VGA, gmode = VGAHI;
	initgraph(&gdriver, &gmode, "bgi");

	for (int i = 0; i < 1; i++)
   {
   	for (int j = 0; j < 1; j++)
      {
      	putpixel(i, j, RED);
      }
   }
   getch();
   getimage(0, 0, 1, 1, data);
   fwrite(data, 1, MAX_IMAGE, image);

	closegraph();

   fclose(image);

   return 0;
}
