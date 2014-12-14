#include <types.h>

bool jp_is_zero(point p) {
	return p.x == 0 && p.y == 0;
}

int32 jp_length_squared(point p) {
	return ((int32)p.x) * p.x + ((int32)p.y) * p.y;
}

int32 jp_distance_squared(point from, point to) {
	point p = jp_point_substract(from, to);
	return jp_length_squared(p);
}

bool jp_rect_contains(point p, int x, int y, int width, int height) {
	return p.x >= x && p.x < x + width && p.y >= y && p.y < y + height;
}

point jp_point_substract(point left, point right) {
	point p;
	p.x = left.x - right.x;
	p.y = left.y - right.y;
	return p;
}

int32 jp_cross_product(point left, point right) {
	return ((int32)left.x) * right.y - ((int32)left.y) * right.x;
}

int32 jp_dot_product(point left, point right) {
	return ((int32)left.x) * right.x + ((int32)left.y) * right.y;
}