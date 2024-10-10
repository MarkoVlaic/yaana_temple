#ifndef YAANA_MODEL_H
#define YAANA_MODEL_H

#include "list.h"
#include "geom.h"

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

void model_init();
void get_walls(struct wall **wa, uint32_t *cnt);
float score_solution(struct object light, struct object mirrors[8], struct vec **path, uint32_t *path_len, struct mirror mirror_result[8], struct vec **score_points_result, uint32_t *score_points_len);

#endif