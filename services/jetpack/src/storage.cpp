#include "storage.h"
#include <string.h>

int jp_init(JPStorage *storage) {
	storage->entries = new LinkedList();

	return 0;
}

int jp_free(JPStorage **storage) {
	delete (*storage);
	return 0;
}

int jp_put(JPStorage *storage, JPEntry *entry) {
	jp_linked_list_add(storage->entries, (void *)entry);
	return 0;
}

int jp_get(JPStorage *storage, const char *key, JPEntry **entry) {
	if (storage->entries->count == 0)
		return -1;

	LinkedListNode *root = storage->entries->root;
	LinkedListNode *current = root;

	do {
		JPEntry *temp = (JPEntry *)current->value;
		if (strstr(temp->key, key)) {
			(*entry) = temp;
			return 0;
		}
	} while ((current = current->next) != root);

	return -1;
}