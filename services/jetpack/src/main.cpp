#include <stdio.h>
#include <mem.h>
#include <malloc.h>
#include "slots.h"
#include "packets.h"
#include "movie.h"

#include <dos.h> // For FP_*
#define FP_L(p) (((int32)(FP_SEG(p)) << 4) + FP_OFF(p))

#define SLOTS 40

const int port = 16742;

JPSlot *slots;

void process_request(JPSlot *slot)
{
	slot->position = slot->data_length = 0;
}

void init_slot(JPSlot *slot)
{
	slot->state = SLOT_Listen;
	slot->position = 0;
	slot->data_length = 0;
	tcp_listen(&slot->socket, port, 0, 0, NULL, 0);
}

void tick_slot(JPSlot *slot, int id)
{
	if (!tcp_tick((sock_type *)&slot->socket))
   {
     	printf("!tcp_tick\n");
     	init_slot(slot);
      return;
   }
	switch (slot->state)
   {
   case SLOT_Listen:
   	if (tcp_established(&slot->socket))
      {
      	printf("Accepted client in slot %d!\n", id);
         slot->state = SLOT_Receive;
      }
      break;
   case SLOT_Receive:
   	jp_slot_read(slot);
      if (slot->position >= sizeof(JPRequest))
      {
       	process_request(slot);
         slot->state = SLOT_Send;
      }
      break;
   case SLOT_Send:
   	jp_slot_write(slot);
      if (slot->position >= slot->data_length)
      	init_slot(slot);
   }
}

void poll() // TODO: free sockets by timeout
{
	static const char wait[] = "-\|/";
   int i = 0;
   for (JPSlot *slot = slots; slot->next; slot = slot->next)
   {
   	printf("%c\r", wait[i++ % 4]);
   	tick_slot(slot, i);
   }
}

void allocate_slots()
{
	JPSlot *slot;
	slots = slot = (JPSlot *)_fmalloc(sizeof(JPSlot));

   for (int i = 1; i < SLOTS; i++)
   {
   	slot->next = (JPSlot *)_fmalloc(sizeof(JPSlot));
      slot = slot->next;
      printf("Allocated %d slots...\n", i + 1);
      printf("Last slot is at %p (%ld).\n", slot, FP_L(slot));
   }
   slot->next = NULL;
   int32 size = FP_L(slot) + sizeof(JPSlot) - FP_L(slots);
   int32 opt_size = (int32)sizeof(JPSlot) * SLOTS;
   printf("All slots occupy %ld bytes (%ld%% of optimal).\n", size, 100 * size / opt_size);
}

void main()
{
	show_image("cirno2.bgi");
	printf("Server started.\n");
	printf("Slot size is %d bytes.\n", sizeof(JPSlot));
   sock_init();
	allocate_slots();
	printf("Memory allocated.\n");
   int count = 0;
	for (JPSlot *slot = slots; slot->next; slot = slot->next)
   {
   	init_slot(slot);
      printf("Initialized %d slots...\n", ++count);
   }
   while (true)
   	poll();
}
