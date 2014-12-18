#include "storage.h"
#include "errors.h"
#include "checkalloc.h"

#include <string.h>

byte jp_hash_heading(JPHeading heading);
int jp_storage_init_cache(JPStorage *storage, JPHeading *cache_buffer, int cache_capacity);
int jp_storage_init_descriptors(JPStorage *storage);
bool jp_lookup_heading(JPStorage *storage, JPHeading heading);
void jp_add_heading(JPStorage *storage, JPHeading heading);
void jp_add_heading_to_cache(JPStorage *storage, JPHeading heading);
void jp_add_id(JPStorage *storage, JPHeading heading, JPID id);

FILE *jp_get_flags_file(JPStorage *storage, byte hash);
FILE *jp_get_headings_cache_file(JPStorage *storage);

JPStorage *jp_storage_init(const char *base_path, JPHeading *cache_buffer, int cache_capacity, log_t log) {
	JPStorage *storage = (JPStorage *)checkalloc(sizeof(JPStorage), log);

	storage->base_path = base_path;
	if (jp_storage_init_cache(storage, cache_buffer, cache_capacity) != JP_ERROR_OK) {
		jp_storage_free(storage);
		return NULL;
	}

	if (jp_storage_init_descriptors(storage) != JP_ERROR_OK) {
		jp_storage_free(storage);
		return NULL;
	}

	return storage;
}

void jp_storage_free(JPStorage *storage) {
	_ffree(storage);
}

int jp_store_path(JPStorage *storage, JPHeading heading, JPID id) {
	if (!jp_lookup_heading(storage, heading))
		jp_add_heading(storage, heading);
	jp_add_id(storage, heading, id);
	return JP_ERROR_OK;
}

int jp_load_ids(JPStorage *storage, JPHeading heading, JPID *ids_buffer, int ids_capacity) {
	byte hash = jp_hash_heading(heading);
	JPHeading temp;
	JPID id;
	FILE *file = jp_get_flags_file(storage, hash);
	int ids_written = 0;

	fseek(file, 0, SEEK_SET);

	while (ids_written < ids_capacity
		&& fread(&temp, sizeof(JPHeading), 1, file) == 1
		&& fread(&id, sizeof(JPID), 1, file) == 1) {
		if (jp_headings_equal(heading, temp)) {
			ids_buffer[ids_written++] = id;
		}
	}

	fclose(file);

	return ids_written;
}

byte jp_hash_heading(JPHeading heading) {
	return (byte)((heading.source.x + heading.source.y) ^ (heading.destination.x + heading.destination.y)
		^ ~((heading.source.x - heading.source.y) ^ (heading.destination.x - heading.destination.y)));
}

int jp_storage_init_cache(JPStorage *storage, JPHeading *cache_buffer, int cache_capacity) {
	FILE *file = jp_get_headings_cache_file(storage);

	storage->cache_buffer = cache_buffer;
	storage->cache_capacity = cache_capacity;
	storage->current_cache_base_index = 0;
	storage->current_cache_items = 0;

	fseek(file, 0, SEEK_SET);
	JPHeading heading;
	while (fread(&heading, sizeof(JPHeading), 1, file) == 1) {
		jp_add_heading_to_cache(storage, heading);
	}
	fclose(file);

	return JP_ERROR_OK;
}

int jp_storage_init_descriptors(JPStorage *storage) {
	for (int i = 0; i < 256; ++i) {
		FILE *file = jp_get_flags_file(storage, i);
		if (file == NULL){
			return JP_ERROR_INVALID_DIRECTORY;
		}
		fclose(file);
	}
	return JP_ERROR_OK;
}

bool jp_lookup_heading(JPStorage *storage, JPHeading heading) {
	for (int i = 0; i < storage->current_cache_items; ++i) {
		int index = (storage->current_cache_base_index + i) % storage->cache_capacity;
		if (jp_headings_equal(heading, storage->cache_buffer[index]))
			return true;
	}
	return false;
}

void jp_add_heading(JPStorage *storage, JPHeading heading) {
	jp_add_heading_to_cache(storage, heading);
	FILE *file = jp_get_headings_cache_file(storage);
	fwrite(&heading, sizeof(JPHeading), 1, file);
	fclose(file);
}

void jp_add_heading_to_cache(JPStorage *storage, JPHeading heading) {
	int index = (storage->current_cache_base_index + storage->current_cache_items) % storage->cache_capacity;
	storage->cache_buffer[index] = heading;
	if (storage->current_cache_items < storage->cache_capacity) {
		storage->current_cache_items++;
	} else {
		storage->current_cache_base_index = (storage->current_cache_base_index + 1) % storage->cache_capacity;
	}
}

void jp_add_id(JPStorage *storage, JPHeading heading, JPID id) {
	byte hash = jp_hash_heading(heading);
	FILE *file = jp_get_flags_file(storage, hash);
	fwrite(&heading, sizeof(JPHeading), 1, file);
	fwrite(&id, sizeof(JPID), 1, file);
	fclose(file);
}

FILE *jp_get_flags_file(JPStorage *storage, byte hash) {
	char buffer[256];
	sprintf(buffer, "%s/%02X.flg", storage->base_path, hash);
	return fopen(buffer, "a+b");
}

FILE *jp_get_headings_cache_file(JPStorage *storage) {
	char buffer[256];
	sprintf(buffer, "%s/headings.csh", storage->base_path);
	return fopen(buffer, "a+b");
}