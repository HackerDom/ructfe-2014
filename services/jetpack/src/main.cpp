#include "map/map.h"
#include "errors.h"

#include <stdio.h>


// int jp_init_map(char *new_map_base_dir);

// int jp_clear_path(point *path, int length);

// int jp_build_path(point source, point destination, point *path);

// int jp_get_bytes(point *path, byte *buffer, int offset, int length);

point segment_buffer[10000L];

int main() {
	char *map_dir = "bin/map";
	if (jp_init_map(map_dir) != JP_ERROR_OK) {
		printf("Failed to initialize map\n");
		return 1;
	}
	point path[100];
	jp_clear_path(path, 100);

	point source, destination;
	source.x = 0;
	source.y = 15;
	destination.x = 100;
	destination.y = 15;

	int errcode = jp_build_path(source, destination, path, segment_buffer);
	if (errcode != JP_ERROR_OK) {
		printf("Failed to build path: %d\n", errcode);
		return 1;
	}

	byte buffer[4 * 100];
	int bytes_written = jp_get_bytes(path, buffer, 0, 4 * 100);
	if (bytes_written > 0) {
		printf("Failed to convert path to bytes\n");
		return 1;
	}

	for (int i = 0; !jp_is_zero(path[i]); ++i) {
		printf("%d %d\n", path[i].x, path[i].y);
	}

	return 0;
}