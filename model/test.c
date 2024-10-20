#include <stdio.h>
#include <stdint.h>

#include "model.h"

int main() {
  model_init();

  struct object light = {
        .pos = { 10.3985761, 4.86143 },
        .angle = 1.70025137
    };


  struct object mirrors[8];

  mirrors[0] = (struct object){
        .pos = { 10.3985761, 4.86143 },
        .angle = 1.70025137
    };
mirrors[1] = (struct object){
        .pos = { 18.1835482, 10.43182225 },
        .angle = 2.63442346
    };
mirrors[2] = (struct object){
        .pos = { 4.93389884, 11.51498573 },
        .angle = 1.33624402
    };
mirrors[3] = (struct object){
        .pos = { 15.76898821, 18.37647013 },
        .angle = 1.61653643
    };
mirrors[4] = (struct object){
        .pos = { 18.00453493, 8.20114528 },
        .angle = 0.22485764
    };
mirrors[5] = (struct object){
        .pos = { 0.42025526, 14.99202899 },
        .angle = 0.83730707
    };
mirrors[6] = (struct object){
        .pos = { 6.73279389, 14.45172173 },
        .angle = 0.71490405
    };
mirrors[7] = (struct object){
        .pos = { 9.13191692, 11.956449 },
        .angle = 2.29161848
    };
mirrors[8] = (struct object){
        .pos = { 14.76218912, 17.1397577 },
        .angle = 2.18813049
    };


  // struct score_arg arg;
    for(int i=0;i<100;i++) {
        float score = score_solution(light, mirrors, NULL);
        printf("score: %f\n", score);
    }
  // for(uint32_t i=0;i<arg.clipped_polygon_size;i++) {
  //   printf("(%f, %f)\n", arg.clipped_polygon[i].x, arg.clipped_polygon[i].y);
  // }

  //score_arg_free(&arg);
}