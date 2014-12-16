#include "map.h"
#include "errors.h"

#include <stdio.h>
#include <string.h>

char *map_base_dir;

void jp_get_region_name(char *buffer, char* base_dir, int x, int y);
int jp_load_region(int region_x, int region_y, point *region_buffer);
void jp_process_region(point source, point destination, point *path, int *path_offset, point *region_buffer);
bool jp_point_satisfy(point source, point destination, point p);
int jp_get_region_x(point p);
int jp_get_region_y(point p);
void jp_swap(int *left, int *right);

int jp_init_map(char *new_map_base_dir) {
	if (new_map_base_dir == NULL)
		return JP_ERROR_INVALID_DIRECTORY;
	char buffer[MAX_BASE_DIR_LENGTH];
	for (int i = 0; i < MAP_WIDTH / MAP_REGION_WIDTH; ++i) {
		for (int j = 0; j < MAP_HEIGHT / MAP_REGION_HEIGHT; ++j) {
			jp_get_region_name(buffer, new_map_base_dir, i, j);
			FILE *file = fopen(buffer, "rb");
			if (file == NULL)
				return JP_ERROR_INVALID_DIRECTORY;
			fclose(file);
		}
	}
	map_base_dir = new_map_base_dir;
	return JP_ERROR_OK;
}

int jp_clear_path(point *path, int length) {
	for (int i = 0; i < length; ++i) {
		path[i].x = path[i].y = 0;
	}
	return JP_ERROR_OK;
}

int jp_build_path(point source, point destination, point *path, point *region_buffer) {
	if (jp_distance_squared(source, destination) > MAX_ALLOWED_DISTANCE * MAX_ALLOWED_DISTANCE)
		return JP_ERROR_DISTANCE_TOO_BIG;
	if (!jp_rect_contains(source, 0, 0, MAP_WIDTH, MAP_HEIGHT))
		return JP_ERROR_INVALID_SOURCE;
	if (!jp_rect_contains(destination, 0, 0, MAP_WIDTH, MAP_HEIGHT))
		return JP_ERROR_INVALID_DESTINATION;

	int min_region_x = jp_get_region_x(source);
	int max_region_x = jp_get_region_x(destination);
	if (min_region_x > max_region_x)
		jp_swap(&min_region_x, &max_region_x);
	int min_region_y = jp_get_region_y(source);
	int max_region_y = jp_get_region_y(destination);
	if (min_region_y > max_region_y)
		jp_swap(&min_region_y, &max_region_y);

	int path_offset = 0;
	for (int i = min_region_x; i <= max_region_x; ++i) {
		for (int j = min_region_y; j <= max_region_y; ++j) {
			if (jp_load_region(i, j, region_buffer) != JP_ERROR_OK)
				return JP_ERROR_DAMAGED_MAP;
			jp_process_region(source, destination, path, &path_offset, region_buffer);
		}
	}

	return JP_ERROR_OK;
}

int jp_get_bytes(point *path, byte *buffer, int offset, int length) {
	int bytes_written = 0;
	point *out_buffer = (point *)(buffer + offset);
	while (!jp_is_zero(*path)) {
		if (bytes_written + 4 > length)
			return bytes_written;
		*out_buffer = *path;
		++out_buffer;
		++path;
	}
	return bytes_written;
}

void jp_get_region_name(char *buffer, char* base_dir, int x, int y) {
	sprintf(buffer, "%s/%04x%04x.map", base_dir, x, y);
}

int jp_load_region(int region_x, int region_y, point *region_buffer) {
	char buffer[MAX_BASE_DIR_LENGTH];
	jp_get_region_name(buffer, map_base_dir, region_x, region_y);
	FILE *file = fopen(buffer, "rb");
	if (file == NULL)
		return JP_ERROR_FAILED_TO_OPEN_REGION;
	point p;
	int current_pointer = 0;
	while (fread(&p, 1, sizeof(point), file) == sizeof(point)) {
		region_buffer[current_pointer++] = p;
	}
	region_buffer[current_pointer].x = 0;
	region_buffer[current_pointer].y = 0;
	fclose(file);
	return JP_ERROR_OK;
}

void jp_process_region(point source, point destination, point *path, int *path_offset, point *region_buffer) {
	for (int i = 0; !jp_is_zero(region_buffer[i]); ++i) {
		if (jp_point_satisfy(source, destination, region_buffer[i])) {
			path[(*path_offset)++] = region_buffer[i];
		}
	}
}

bool jp_point_satisfy(point source, point destination, point p) {
	point a = jp_point_substract(destination, source);
	point b = jp_point_substract(p, source);
	point c = jp_point_substract(destination, p);
	int32 a_b_cp = jp_cross_product(a, b);
	int32 a_b_dp = jp_dot_product(a, b);
	int32 a_c_dp = jp_dot_product(a, c);

	return a_b_cp * a_b_cp < MAX_ALLOWED_WIDTH * MAX_ALLOWED_WIDTH * jp_length_squared(a) && a_b_dp >= 0 && a_c_dp >= 0;
}

int jp_get_region_x(point p) {
	return p.x / MAP_REGION_WIDTH;
}

int jp_get_region_y(point p) {
	return p.y / MAP_REGION_HEIGHT;
}

void jp_swap(int *left, int *right) {
	*left = (*left) ^ (*right);
	*right = (*left) ^ (*right);
	*left = (*left) ^ (*right);
}