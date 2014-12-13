#ifndef JETPACK_LINKED_LIST
#define JETPACK_LINKED_LIST

struct LinkedListNode {
	void *value;
	LinkedListNode *next, *prev;
};

struct LinkedList {
	LinkedListNode *root;
	int count;
};
void jp_linked_list_add(LinkedList *list, void *value);

void jp_linked_list_remove(LinkedList *list, LinkedListNode *node);

void jp_linked_list_free(LinkedList * list);

#endif