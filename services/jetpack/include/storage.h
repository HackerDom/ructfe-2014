#ifndef JETPACK_STORAGE_H
#define JETPACK_STORAGE_H

#include <linked_list.h>

struct JPEntry {
	char key[16];
	char value[16];
};

struct JPStorage
{
	LinkedList *entries;
};


int jp_init(JPStorage *storage);

int jp_free(JPStorage *storage);

int jp_put(JPStorage *storage, JPEntry *entry);

int jp_get(JPStorage *storage, const char *key, JPEntry **entry);

#endif