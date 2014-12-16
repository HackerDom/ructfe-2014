#ifndef JETPACK_PACKETS_H
#define JETPACK_PACKETS_H

#include "types.h"

typedef byte[32] JPID;

enum JPRequestType
{
	REQ_Put,
	REQ_Get
};

#define JP_PUT_SIZE 41
#define JP_GET_SIZE 9

struct JPRequest
{
	byte type;
	point source;
	point destination;
	JPID id;
};

struct JPPutResponse
{
	int16 code;
	point *path;
};

struct JPGetResponse
{
	int16 code;
	JPID *ids;
};

#endif