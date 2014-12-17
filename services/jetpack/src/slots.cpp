extern "C" {
#include <wattcp.h>
}
#include "slots.h"

int16 jp_slot_read(JPSlot *slot)
{
	if (slot->state != SLOT_Receive)
   	return -1;
   int16 bytes_read = sock_fastread((sock_type *)&slot->socket, slot->buffer + slot->position, SLOT_BUFFER - slot->position);
   slot->position += bytes_read;
   return bytes_read;
}

int16 jp_slot_write(JPSlot *slot)
{
	if (slot->state != SLOT_Send)
   	return -1;
   int16 bytes_written = sock_fastwrite((sock_type *)&slot->socket, slot->buffer + slot->position, slot->data_length - slot->position);
   slot->position += bytes_written;
   return bytes_written;
}