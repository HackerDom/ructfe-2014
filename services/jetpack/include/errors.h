#ifndef JETPACK_ERRORS_H
#define JETPACK_ERRORS_H

enum JPError
{
	JP_ERROR_FAILED_TO_OPEN_REGION = -6,
	JP_ERROR_DAMAGED_MAP,
	JP_ERROR_INVALID_DIRECTORY,
	JP_ERROR_INVALID_SOURCE,
	JP_ERROR_INVALID_DESTINATION,
	JP_ERROR_DISTANCE_TOO_BIG,
	JP_ERROR_OK
};

#endif