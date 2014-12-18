#ifndef JETPACK_STORAGE_H
#define JETPACK_STORAGE_H

#include <stdio.h>

#include "types.h"
#include "logging.h"

struct JPStorage
{
	const char *base_path;

	JPHeading *cache_buffer;
	int cache_capacity;
	int current_cache_base_index;
	int current_cache_items;
};

JPStorage *jp_storage_init(const char *base_path, JPHeading *cache_buffer, int cache_capacity, log_t log);

void jp_storage_free(JPStorage *storage);

int jp_store_path(JPStorage *storage, JPHeading heading, JPID id);

int jp_load_ids(JPStorage *storage, JPHeading heading, JPID *ids_buffer, int ids_capacity);

#endif