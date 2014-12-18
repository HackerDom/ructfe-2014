#include <stdio.h>
#include <mem.h>
#include <conio.h>
#include <string.h>
#include "slots.h"
#include "packets.h"
#include "movie.h"
#include "storage.h"
#include "map.h"
#include "checkalloc.h"

#include <dos.h> // For FP_*
#define FP_L(p) (((int32)(FP_SEG(p)) << 4) + FP_OFF(p))

#define SLOTS 40
#define SLOT_TIMEOUT 3000

#define MAX_OPLOG 8000
#define MAX_PATH 64
#define MAX_IDS 100
#define MAX_MAP 2000

const int port = 16742;

JPStorage *storage;

JPSlot *slots;

point *path_buffer;

JPHeading *oplog_buffer;

point *map_chunk;

JPID *ids_buffer;

log_t log;

void respond_error(JPSlot *slot, int code)
{
	jp_logp(log, slot->name, "Returning error: %d.", code);
	*(int *)slot->buffer = code;
	slot->data_length = 2;
}

void process_request(JPSlot *slot)
{
	JPRequest *request = (JPRequest *)slot->buffer;
	int ret, count, bytes;
	switch (request->type)
	{
	case REQ_Put:
		jp_logp(log, slot->name, "Received PUT request, calculating path from (%d, %d) to (%d, %d).",
		request->source.x, request->source.y, request->destination.x, request->destination.y);
		jp_clear_path(path_buffer, MAX_PATH);
		ret = jp_build_path(request->source, request->destination, path_buffer, map_chunk);
		if (ret)
			respond_error(slot, ret);
		else
		{
			jp_store_path(storage, *(JPHeading *)&request->source, request->id);
			bytes = jp_get_bytes(path_buffer, slot->buffer, 2, SLOT_BUFFER - 2);
			jp_logp(log, slot->name, "Returning %d path nodes.", bytes / sizeof(point));
			*(int *)slot->buffer = bytes;
			slot->data_length = bytes + 2;
		}
		break;
	case REQ_Get:
		jp_logp(log, slot->name, "Received GET request for path (%d, %d) -> (%d, %d).", 
		request->source.x, request->source.y, request->destination.x, request->destination.y);
		count = jp_load_ids(storage, *(JPHeading *)&request->source, ids_buffer, MAX_IDS);
		_fmemcpy(slot->buffer + 2, ids_buffer, SLOT_BUFFER - 2);
		jp_logp(log, slot->name, "Returning %d IDs.", count);
		*(uint16 *)slot->buffer = count * sizeof(JPID);
		slot->data_length = count * sizeof(JPID) + 2;
		break;
	default:
		jp_logp(log, slot->name, "Received unrecognized request.");
		slot->data_length = 0;
	}
	slot->position = 0;
}

void init_slot(JPSlot *slot)
{
	slot->state = SLOT_Listen;
	slot->position = 0;
	slot->data_length = 0;
	tcp_listen(&slot->socket, port, 0, 0, NULL, 0);
}

void reset_slot(JPSlot *slot)
{
	sock_close((sock_type *)&slot->socket);
	init_slot(slot);
}

void tick_slot(JPSlot *slot, int id)
{
	if (!tcp_tick((sock_type *)&slot->socket) ||
		(slot->state != SLOT_Listen && clock() - slot->accept_time > SLOT_TIMEOUT))
	{
		jp_log(log, "Resetting erroneous or timed-out slot %d.", id);
		reset_slot(slot);
		return;
	}
	int ret;
	switch (slot->state)
	{
	case SLOT_Listen:
		if (tcp_established(&slot->socket))
		{
			jp_log(log, "Accepted client in slot %d!", id);
			slot->state = SLOT_Receive;
			slot->accept_time = clock();
		}
		break;
	case SLOT_Receive:
		ret = jp_slot_read(slot);
		if (ret < 0)
		{
			reset_slot(slot);
			return;
		}
		if (slot->position >= 2)
		{
			int needed_size = ((JPRequest *)slot->buffer)->type == REQ_Put ? JP_PUT_SIZE : JP_GET_SIZE;
			if (slot->position >= needed_size)
			{
				process_request(slot);
				slot->state = SLOT_Send;
			}
		}
		break;
	case SLOT_Send:
		ret = jp_slot_write(slot);
		if (ret < 0 || slot->position >= slot->data_length)
			 reset_slot(slot);
		 break;
	}
}

bool poll()
{
	if (kbhit() && getch() == 27)
		return false;
	static const char wait[] = "-\|/";
	int i = 0;
	for (JPSlot *slot = slots; slot->next; slot = slot->next)
	{
		printf("%c\r", wait[i++ % 4]);
		tick_slot(slot, i);
	}
	return true;
}

void allocate_slots()
{
	JPSlot *slot;
	slots = slot = (JPSlot *)checkalloc(sizeof(JPSlot), log);

	for (int i = 1; i < SLOTS; i++)
	{
		slot->next = (JPSlot *)checkalloc(sizeof(JPSlot), log);
		slot = slot->next;
		jp_log(log, "Allocated %d slots...", i + 1);
		jp_log(log, "Last slot is at %p (%ld).", slot, FP_L(slot));
	}
	slot->next = NULL;
	int32 size = FP_L(slot) + sizeof(JPSlot) - FP_L(slots);
	int32 opt_size = (int32)sizeof(JPSlot) * SLOTS;
	jp_log(log, "All slots occupy %ld bytes (%ld%% of optimal).", size, 100 * size / opt_size);
}

void allocate_memory()
{
	jp_log(log, "Slot size is %d bytes.", sizeof(JPSlot));
	allocate_slots();
	path_buffer = (point *)checkalloc(sizeof(point) * MAX_PATH, log);
	oplog_buffer = (JPHeading *)checkalloc(sizeof(JPHeading) * MAX_OPLOG, log);
	//printf("path_buffer is at %08lx, oplog_buffer is at %08lx\n", FP_L(path_buffer), FP_L(oplog_buffer));
	//printf("distance is %ld bytes\n", FP_L(oplog_buffer) - FP_L(path_buffer) - sizeof(point) * MAX_PATH);
	map_chunk = (point *)checkalloc(sizeof(point) * MAX_MAP, log);
	ids_buffer = (JPID *)checkalloc(sizeof(JPID) * MAX_IDS, log);
	storage = jp_storage_init("store", oplog_buffer, MAX_OPLOG, log);
	log = jp_open_log("jetpack.log");
	int ret = jp_init_map("map");
	if (ret)
		jp_log(log, "Error: jp_init_map returned %d.", ret);
	jp_log(log, "Memory allocated.");
}

void cleanup()
{
	jp_storage_free(storage);
	jp_close_log(log);
}

void show_intro()
{
	jp_show_movie("jetpack.mov", log);
}

void main(int argc, const char **argv)
{
	if (argc > 1 && !stricmp(argv[1], "--intro"))
	show_intro();
	jp_log(log, "Server started.");
	sock_init();
	allocate_memory();
	int count = 0;
	for (JPSlot *slot = slots; slot->next; slot = slot->next)
	{
		init_slot(slot);
		sprintf(slot->name, "SLOT %02d", count);
		jp_log(log, "Initialized %d slots...", ++count);
	}
	while (poll()) ;
	cleanup();
	jp_log(log, "Exiting server...");
}
