#include <stdio.h>
#include <stdint.h>

#include "model.h"

int main() {
  model_init();

  struct object light = {
    .pos = { 5, 5},
    .angle = 0.26
  };

  struct object mirrors[8];

  mirrors[0] = (struct object) {
            .pos = { 0.5, 0.5 },
            .angle = 0.26
         };
mirrors[1] = (struct object) {
            .pos = { 0.5, 0.5 },
            .angle = 0.26
         };
mirrors[2] = (struct object) {
            .pos = { 0.5, 0.5 },
            .angle = 0.26
         };
mirrors[3] = (struct object) {
            .pos = { 0.5, 0.5 },
            .angle = 0.26
         };
mirrors[4] = (struct object) {
            .pos = { 0.5, 0.5 },
            .angle = 0.26
         };
mirrors[5] = (struct object) {
            .pos = { 0.5, 0.5 },
            .angle = 0.26
         };
mirrors[6] = (struct object) {
   .pos = { 0.5, 0.5 },
   .angle = 0.26
};
mirrors[7] = (struct object) {
            .pos = { 0.5, 0.5 },
            .angle = 0.26
         };
  // struct score_arg arg;

  float score = score_solution(light, mirrors, NULL);
  printf("score: %f\n", score);
  // for(uint32_t i=0;i<arg.clipped_polygon_size;i++) {
  //   printf("(%f, %f)\n", arg.clipped_polygon[i].x, arg.clipped_polygon[i].y);
  // }

  //score_arg_free(&arg);
}