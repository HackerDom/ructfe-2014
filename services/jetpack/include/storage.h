#ifndef JETPACK_STORAGE_H
#define JETPACK_STORAGE_H

#include "types.h"

struct JPStorage
{
	// ...
};

JPStorage *jp_storage_init(const char *base_path, JPHeading *oplog_buffer, int oplog_capacity);

void jp_storage_free(JPStorage *storage);

int jp_store_path(JPStorage *storage, JPHeading heading, JPID id);

int jp_load_ids(JPStorage *storage, JPHeading heading, JPID *ids_buffer, int ids_capacity);

#endif