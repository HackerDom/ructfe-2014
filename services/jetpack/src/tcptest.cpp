extern "C" {
#include <wattcp.h>
}
#include <stdio.h>
#include <mem.h>

enum SlotState
{
	SLOT_LISTEN = 0,
   SLOT_REQUEST
};

#define SLOTS 1024
#define RECV_BUF 256

struct Slot
{
	sock_type *socket;
	int state;
   int read_pos;
   byte *buffer;
} slots[SLOTS];

static const int port = 16742;

void reset_slot(Slot *slot)
{
	slot->state = SLOT_LISTEN;
   slot->read_pos = 0;
   sock_mode(slot->socket, TCP_MODE_ASCII);
	tcp_listen(&slot->socket->tcp, port, 0, 0, NULL, 0);
}

void init_slot(Slot *slot)
{
	memset(slot, 0, sizeof(Slot));
   slot->socket = (sock_type *)new tcp_Socket;
   slot->buffer = new byte[RECV_BUF];
   sock_mode(slot->socket, TCP_MODE_ASCII);
	tcp_listen(&slot->socket->tcp, port, 0, 0, NULL, 0);
}

bool fastgets(Slot *slot)
{
	int bytes_read = sock_fastread(slot->socket, slot->buffer + slot->read_pos, RECV_BUF - 1 - slot->read_pos);
   for (int i = slot->read_pos; i < slot->read_pos + bytes_read; i++)
   {
   	if (slot->buffer[i] == '\n')
      {
			slot->buffer[i] = 0;
         return true;
      }
   }
	slot->read_pos += bytes_read;
   return slot->read_pos == RECV_BUF - 1;
}

void poll() // TODO: free sockets by timeout
{
	static const char wait[] = "-\|/";
   for (int i = 0; i < SLOTS; i++)
   {
   	printf("%c\r", wait[i % 4]);
   	if (!tcp_tick(slots[i].socket))
      {
      	printf("!tcp_tick\n");
      	reset_slot(&slots[i]);
         continue;
      }
		switch (slots[i].state)
      {
   	case SLOT_LISTEN:
      	if (tcp_established(&slots[i].socket->tcp))
         {
         	printf("Accepted client in slot %d!\n", i);
         	slots[i].state = SLOT_REQUEST;
         }
         else
         	break;
      case SLOT_REQUEST:
			if (fastgets(&slots[i]))
         {
         	sock_puts(slots[i].socket, slots[i].buffer); //TODO: full asynchrony
				sock_close(slots[i].socket);
				reset_slot(&slots[i]);
         }
      }
   }
}

void main()
{
	//tcp_set_debug_state(9);
   sock_init();
	for (int i = 0; i < SLOTS; i++)
   {
   	init_slot(&slots[i]);
      printf("Allocated %d slots...", i + 1);
   }
   while (true)
   	poll();
}