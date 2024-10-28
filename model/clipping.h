#ifndef YAANA_CLIPPING_H
#define YAANA_CLIPPING_H

#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

#include "model_data.h"

typedef void* polygon_t;
typedef void* polygon_vec_t;

EXTERNC void clipping_add_wall(struct wall *w);
EXTERNC polygon_t polygon_new();
EXTERNC void polygon_free(polygon_t rect_vec);
EXTERNC void polygon_add_point(polygon_t rect, struct vec point);
EXTERNC polygon_vec_t polygon_union_rect(polygon_vec_t polygon, polygon_t rect);
EXTERNC polygon_t polygon_clip_walls(polygon_vec_t polygon);
EXTERNC float polygon_area(polygon_vec_t polygon);
EXTERNC void polygon_to_points(polygon_vec_t polygon, struct vec **points, uint32_t *cnt);

#endif