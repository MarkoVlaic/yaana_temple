#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

#define ITERATIONS 1e8

#include "model.h"

float randf() {
  return (float) rand() / (float) RAND_MAX;
}

struct object random_object() {
  struct object result;
  result.pos.x = randf() * 20;
  result.pos.y = randf() * 20;
  result.angle = randf() * 2 * PI;

  return result;
}

int main() {
  model_init();
  srand(time(NULL));

  struct object light;
  struct object mirrors[8];

  for(int i=0;i<ITERATIONS;i++) {
    light = random_object();
    for(int j=0;j<8;j++) {
      mirrors[j] = random_object();
    }
    score_solution(light, mirrors, NULL);
  }

}