#include "linked_list.h"

void jp_linked_list_add(LinkedList *list, void *value) {
	LinkedListNode *root = list->root;
	LinkedListNode *node = new LinkedListNode();
	node->value = value;
	if (list->count == 0) {
		list->root = node;
	} else {
		node->prev = root->prev;
		node->next = root;

		root->prev->next = node;
		root->prev = node;
	}
	++list->count;
}

void jp_linked_list_remove(LinkedList *list, LinkedListNode *node) {
	if (list->count == 0)
		return;
	if (list->count == 1){
		list->root = 0;
	} else {
		node->prev->next = node->next;
		node->next->prev = node->prev;
	}
	delete node;
}