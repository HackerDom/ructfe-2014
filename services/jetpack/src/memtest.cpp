#include <stdio.h>
#include "types.h"

byte __huge data[512 * 1024L];

void main()
{
	printf("Our data is at %p\n", data);
	//printf("Our code is at %p\n", main);
}