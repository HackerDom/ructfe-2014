#ifndef JETPACK_CHECKALLOC_H
#define JETPACK_CHECKALLOC_H

#include <malloc.h>
#include "types.h"
#include "logging.h"

void *checkalloc(size_t size, log_t log);

#endif