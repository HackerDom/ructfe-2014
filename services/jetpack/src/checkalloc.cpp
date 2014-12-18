#include <stdio.h>
#include <stdlib.h>
#include <mem.h>
#include "checkalloc.h"
#include "logging.h"

void *checkalloc(size_t size, log_t log)
{
	void *mem = _fmalloc(size);
	if (!mem)
	{
		printf("Failed to allocate %ld bytes!\n", size);
		jp_log(log, "Failed to allocate %ld bytes!\n", size);
		exit(1);
	}
	_fmemset(mem, 0, size);
	return mem;
}