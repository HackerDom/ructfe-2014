#include <stdio.h>
#include <stdlib.h>
#include <mem.h>
#include "checkalloc.h"

void *checkalloc(size_t size)
{
	void *mem = _fmalloc(size);
	if (!mem)
	{
		printf("Failed to allocate %ld bytes!\n", size);
		exit(1);
	}
   _fmemset(mem, 0, size);
   for (int i = 0; i < size; i++)
   if (*((byte *)mem + i))
   {
   	printf("Allocated memory is not zero!\n");
      exit(1);
   }
	return mem;
}