#include <stdio.h>
#include <stdint.h>

#include "model.h"

int main() {
  model_init();

  float x, y;
  random_lamp(&x, &y);
  printf("%f %f\n", x, y);

  // struct object light = {.pos = {.x = 1.00525033, .y = 17.9279232}, .angle = 1.88850057};

  // struct object mirrors[8];
  //  mirrors[0] = (struct object) {.pos = {.x = 0.121660233, .y = 0.410045624}, .angle = 5.45028543};
  //  mirrors[1] = (struct object) {.pos = {.x = 0.0612931624, .y = 0.236988366}, .angle = 1.87766623};
  //  mirrors[2] = (struct object) {.pos = {.x = 0.981837034, .y = 0.0701729879}, .angle = 2.76210737};
  //  mirrors[3] = (struct object) {.pos = {.x = 0.292955428, .y = 0.537986577}, .angle = 4.79908895};
  //  mirrors[4] = (struct object) {.pos = {.x = 0.0171479601, .y = 0.971392691}, .angle = 1.31264007};
  //  mirrors[5] = (struct object) {.pos = {.x = 0.686172605, .y = 0.960252702}, .angle = 0.172423825};
  //  mirrors[6] = (struct object) {.pos = {.x = 0.91086942, .y = 0.753861725}, .angle = 5.11454725};
  //  mirrors[7] = (struct object) {.pos = {.x = 0.335205376, .y = 0.367806911}, .angle = 5.81290102};

  //  struct mirror mirror_result[8];
  // // struct score_arg arg;
  //   for(int i=0;i<100;i++) {
  //       float score = score_solution(light, mirrors, mirror_result, NULL);
  //       printf("score: %f\n", score);
  //   }
  // for(uint32_t i=0;i<arg.clipped_polygon_size;i++) {
  //   printf("(%f, %f)\n", arg.clipped_polygon[i].x, arg.clipped_polygon[i].y);
  // }

  //score_arg_free(&arg);
}