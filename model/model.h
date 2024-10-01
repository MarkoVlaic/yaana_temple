#include "list.h"

struct wall {
  float x;
  float y;
  float w;
  float h;

  LIST_ENTRY(wall) next_wall;
};

void model_init();
void get_walls(struct wall **wa, uint32_t *cnt);