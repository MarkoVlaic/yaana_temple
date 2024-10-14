#include <stdio.h>
#include <stdint.h>

#define ITERATIONS 1e4

#include "model.h"

int main() {
  model_init();

  struct object light = {
    .pos = { 5, 5 },
    .angle = 0.26
  };

  struct object mirrors[8];

  mirrors[0] = (struct object) {
    .pos = { 11.5, 6.5 },
    .angle = 0.9
  };
  
  mirrors[1] = (struct object) {
    .pos = { 11.9, 16.5 },
    .angle = 0.95
  };

  mirrors[2] = (struct object) {
    .pos = { 15.2, 17.6 },
    .angle = 2.45
  };

  mirrors[3] = (struct object) {
    .pos = { 13.8, 12.0 },
    .angle = 0.92
  };

  mirrors[4] = (struct object) {
    .pos = { 1.6, 6.2 },
    .angle = 2.53
  };

  mirrors[5] = (struct object) {
    .pos = { 2.2, 14.7 },
    .angle = 0.66
  };

  mirrors[6] = (struct object) {
    .pos = { 18, 12 },
    .angle = 1.6
  };

  mirrors[7] = (struct object) {
    .pos = { 13.8, 11.5 },
    .angle = -0.54
  };

  for(int i=0;i<ITERATIONS;i++) {
    score_solution(light, mirrors, NULL);
  }

}