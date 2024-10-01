#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "model.h"
#include "list.h"

char map[20][20] = {
  "OOOOOOOOOOOOOOOOOOOO",
  "O....O........O....O",
  "O.......O..O.......O",
  "O.....O......O.....O",
  "O..O.....OO.....O..O",
  "OO.......OO.......OO",
  "O...O..........O...O",
  "O......O....O......O",
  "O........OO........O",
  "O.O..OO......OO..O.O",
  "O.O..OO......OO..O.O",
  "O........OO........O",
  "O......O....O......O",
  "O...O..........O...O",
  "OO.......OO.......OO",
  "O..O.....OO.....O..O",
  "O.....O......O.....O",
  "O.......O..O.......O",
  "O....O........O....O",
  "OOOOOOOOOOOOOOOOOOOO"
};

static LIST_HEAD(wall_list, wall) walls = LIST_HEAD_INIT();

void model_init() {
  bool processed[20][20];
  struct wall *next_wall;
  int i, j, k, w;
  float potential_w, potential_h;

  for(i = 0; i < 20; i++) {
    for(j = 0; j < 20; j++) {
      processed[i][j] = false;
    }
  }

  for(i = 0; i < 20; i++) {
    for(j = 0; j < 20; j++) {
      if(map[i][j] == 'O' && !processed[i][j]) {
        next_wall = malloc(sizeof(next_wall));
        next_wall->x = j;
        next_wall->y = 20 - i; 
        
        k = i;
        while(k < 20 && map[k][j] == 'O' && !processed[k][j]) {
          k++;
        }
        potential_h = k - i;

        k = j;
        while(k < 20 && map[i][k] == 'O' && !processed[i][k]) {
          k++;
        }
        potential_w = k - j;

        if(potential_h > potential_w) {
          next_wall->h = potential_h;
          next_wall->w = 0;
          for(k = j;k < 20 && map[i][k] == 'O' && !processed[i][k];k++) {
            bool full = true;
            for(w = i; w < i + potential_h; w++) {
              if(map[w][k] != 'O' || processed[w][k]) {
                full = false;
                break;
              }
            }

            if(!full) {
              break;
            }
            next_wall->w++;
          }
        } else {
          next_wall->w = potential_w;
          next_wall->h = 0;
          for(k = i;k < 20 && map[k][j] == 'O' && !processed[k][j];k++) {
            bool full = true;
            for(w = j; w < j + potential_w; w++) {
              if(map[k][w] != 'O' || processed[k][w]) {
                full = false;
                break;
              }
            }

            if(!full) {
              break;
            }
            next_wall->h++;
          }
        }

        for(k = i;k < i + next_wall->h; k++) {
          for(w = j; w < j + next_wall->w; w++) {
            processed[k][w] = true;
          }
        }

        LIST_INSERT(&walls, next_wall, next_wall);
      }
    }
  }
}

void get_walls(struct wall **wa, uint32_t *cnt) {
  uint32_t size = LIST_SIZE(&(walls));
  *cnt = size;
  *wa = malloc(sizeof(struct wall) * size);
  struct wall *w;
  int i = 0;
  
  LIST_FOREACH(w, &walls, next_wall) {
    memcpy(&((*wa)[i]), w, sizeof(struct wall));
    i++;
  }
}