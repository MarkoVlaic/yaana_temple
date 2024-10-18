#include <stdio.h>
#include <stdint.h>

#include "model.h"

int main() {
  model_init();

  struct object light = {
    .pos = { 16.5442638, 3.82861733},
    .angle = 4.37968731
  };

  struct object mirrors[8];

  mirrors[0] = (struct object) {
            .pos = { 11.6856909, 6.5166831 },
            .angle = 1.66598213
         };
mirrors[1] = (struct object) {
            .pos = { 3.43560505, 10.2965584 },
            .angle = 0.871678054
         };
mirrors[2] = (struct object) {
            .pos = { 9.70941448, 12.3708687 },
            .angle = 3.75155759
         };
mirrors[3] = (struct object) {
            .pos = { 4.07741928, 11.7029171 },
            .angle = 1.66413093
         };
mirrors[4] = (struct object) {
            .pos = { 15.9491453, 14.3437719 },
            .angle = 2.82717705
         };
mirrors[5] = (struct object) {
            .pos = { 11.0879555, 12.4287834 },
            .angle = 5.95866919
         };
mirrors[6] = (struct object) {
            .pos = { 2.29543543, 6.57751131 },
            .angle = 5.07053852
         };
mirrors[7] = (struct object) {
            .pos = { 6.62103939, 12.3743782 },
            .angle = 1.85373354
         };

  // struct score_arg arg;

  float score = score_solution(light, mirrors, NULL);
  printf("score: %f\n", score);
  // for(uint32_t i=0;i<arg.clipped_polygon_size;i++) {
  //   printf("(%f, %f)\n", arg.clipped_polygon[i].x, arg.clipped_polygon[i].y);
  // }

  //score_arg_free(&arg);
}