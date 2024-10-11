#ifndef YAANA_CLIPPING_H
#define YAANA_CLIPPING_H

#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

#include "model_data.h"

EXTERNC void clipping_add_wall(struct wall *w);

#endif