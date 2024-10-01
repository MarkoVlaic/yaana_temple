#include <stdio.h>
#include <stdint.h>

#include "model.h"

int main() {
  model_init();

  struct wall *walls;
  uint32_t size;
  get_walls(&walls, &size);
  printf("get walls returned %d:\n", size);
  struct wall *wl;
  for(int i=0;i<size;i++) {
    wl = &walls[i];
    printf("x = %f | y = %f | w = %f | h = %f\n", wl->x, wl->y, wl->w, wl->h);
  }
}