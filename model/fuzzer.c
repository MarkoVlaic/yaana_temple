#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

#define ITERATIONS 1e3

#include "model.h"

float randf() {
  return (float) rand() / (float) RAND_MAX;
}

struct object random_light() {
  struct object result = {
    .pos = { randf() * 20, randf() * 20 },
    .angle = randf() * 2 * PI
  };

  return result;
}

struct object random_object() {
  struct object result;
  result.pos.x = randf();
  result.pos.y = randf();
  result.angle = randf() * 2 * PI;

  return result;
}

int main() {

  model_init();
  srand(time(NULL));

  struct object light;
  struct object mirrors[8];
  struct mirror mirror_result[8];

  for(int i=0;i<ITERATIONS;i++) {
    light = random_light();
    for(int j=0;j<8;j++) {
      mirrors[j] = random_object();
    }
    double score = score_solution(light, mirrors, mirror_result, NULL);
    printf("score: %f\n", score);
  }

}