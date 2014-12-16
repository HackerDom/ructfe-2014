#ifndef JETPACK_TYPES_H
#define JETPACK_TYPES_H

typedef unsigned char byte;
typedef int int16;
typedef unsigned int uint16;
typedef long int32;
typedef unsigned long uint32;

struct JPPoint
{
	int16 x;
	int16 y;
};

typedef JPPoint point;

struct JPPath
{
	point source;
	point destination;
};

#endif