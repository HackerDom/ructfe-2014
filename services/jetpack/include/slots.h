#ifndef JETPACK_SLOTS_H
#define JETPACK_SLOTS_H

extern "C" {
#include <wattcp.h>
}
#include <time.h>
#include "types.h"

#define SLOT_BUFFER 4096

enum JPSlotState
{
	SLOT_Listen = 0,
	SLOT_Receive,
	SLOT_Send
};

struct JPSlot
{
	int16 state;
	int16 position;
	int16 data_length;
	clock_t accept_time;
	JPSlot *next;
	char name[16];
	tcp_Socket socket;
	byte buffer[SLOT_BUFFER];
};

int16 jp_slot_read(JPSlot *slot);
int16 jp_slot_write(JPSlot *slot);

#endif