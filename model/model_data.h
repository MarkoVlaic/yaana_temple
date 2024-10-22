#ifndef YAANA_MODEL_DATA_H
#define YAANA_MODEL_DATA_H

#include "geom.h"
#include "list.h"

struct wall {
  struct vec pos;
  float w;
  float h;

  
  struct vec verts[4];
  struct segment segments[4];

  LIST_ENTRY(wall) next_wall;
};

struct mirror {
  struct vec start;
  struct vec end;
  struct segment seg;
  float angle;
  struct vec dir;
  struct vec normal;
};

struct score_arg {
  struct vec *path;
  uint32_t path_len;
  struct vec *score_rects;
  uint32_t score_rects_len;
  struct vec *clipped_polygon;
  uint32_t clipped_polygon_size;
};

#endif