#ifndef JETPACK_TYPES_H
#define JETPACK_TYPES_H

typedef unsigned char byte;
typedef int int16;
typedef unsigned int uint16;
typedef long int32;
typedef unsigned long uint32;

struct JPID
{
	byte data[32];
};

struct JPPoint
{
	int16 x;
	int16 y;
};

typedef JPPoint point;

struct JPHeading
{
	point source;
	point destination;
};

bool jp_is_zero(point p);

int32 jp_length_squared(point p);

int32 jp_distance_squared(point from, point to);

bool jp_rect_contains(point p, int x, int y, int width, int height);

point jp_point_substract(point left, point right);

int32 jp_cross_product(point left, point right);

int32 jp_dot_product(point left, point right);

bool jp_headings_equal(JPHeading left, JPHeading right);

#endif