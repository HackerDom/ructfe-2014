#ifndef JETPACK_PACKETS_H
#define JETPACK_PACKETS_H

#include "types.h"

#define RESP_OK 0
#define RESP_OUT_OF_RANGE -1
#define RESP_TOO_FAR -2

struct JPRequest
{
	point source;
	point destination;
};

struct JPResponse
{
	int16 code;
	point *path;
};

#endif