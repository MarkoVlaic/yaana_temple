#define __USE_MISC

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "geom.h"
#include "model.h"
#include "list.h"
#include "clipping.h"

#define MAP_SIDE 20
#define WALL_SIDE 1
#define MIRROR_LENGTH 0.5f
#define EPSILON 1e-4
#define FREE_SPACE_AREA 272.0f
#define LOOP_ITER_THRESHOLD 100000

char map[MAP_SIDE + 1][MAP_SIDE + 1] = {
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

static void preprocess_walls() {
  struct wall *w;

  LIST_FOREACH(w, &walls, next_wall) {
    w->verts[0] = w->pos; // top left
    w->verts[1] = vec_add(w->pos, (struct vec) { w->w, 0 }); // top right
    w->verts[2] = vec_add(w->pos, (struct vec) { w->w, -w->h }); // bottom right
    w->verts[3] = vec_add(w->pos, (struct vec) { 0, -w->h }); // bottom left

    w->segments[0] = segment_new(w->verts[0], 0, w->w);
    w->segments[1] = segment_new(w->verts[0], -PI/2, w->h);
    w->segments[2] = segment_new(w->verts[2], PI/2, w->h);
    w->segments[3] = segment_new(w->verts[2], PI, w->w);

    clipping_add_wall(w);
  }
}

void model_init() {
  bool processed[MAP_SIDE][MAP_SIDE];
  struct wall *next_wall;
  int i, j, k, w;
  float potential_w, potential_h;

  for(i = 0; i < MAP_SIDE; i++) {
    for(j = 0; j < MAP_SIDE; j++) {
      processed[i][j] = false;
    }
  }

  for(i = 0; i < MAP_SIDE; i++) {
    for(j = 0; j < MAP_SIDE; j++) {
      if(map[i][j] == 'O' && !processed[i][j]) {
        next_wall = (struct wall *) malloc(sizeof(struct wall));
        next_wall->pos.x = j;
        next_wall->pos.y = MAP_SIDE - i; 
        
        k = i;
        while(k < MAP_SIDE && map[k][j] == 'O' && !processed[k][j]) {
          k++;
        }
        potential_h = k - i;

        k = j;
        while(k < MAP_SIDE && map[i][k] == 'O' && !processed[i][k]) {
          k++;
        }
        potential_w = k - j;

        if(potential_h > potential_w) {
          next_wall->h = potential_h;
          next_wall->w = 0;
          for(k = j;k < MAP_SIDE && map[i][k] == 'O' && !processed[i][k];k++) {
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
          for(k = i;k < MAP_SIDE && map[k][j] == 'O' && !processed[k][j];k++) {
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

  preprocess_walls();
}

void get_walls(struct wall **wa, uint32_t *cnt) {
  uint32_t size = LIST_SIZE(&(walls));
  *cnt = size;
  *wa = (struct wall *) malloc(sizeof(struct wall) * size);
  struct wall *w;
  int i = 0;
  
  LIST_FOREACH(w, &walls, next_wall) {
    memcpy(&((*wa)[i]), w, sizeof(struct wall));
    i++;
  }
}

static void preprocess_mirror(struct object mirror_obj, struct mirror *mirror) {
  struct vec dir = { cosf(mirror_obj.angle), sinf(mirror_obj.angle) };
  struct vec normal = { -dir.y, dir.x };
  *mirror = (struct mirror) {
    .start = mirror_obj.pos,
    .end = vec_add(mirror_obj.pos, vec_mul(dir, MIRROR_LENGTH)),
    .seg = segment_new(mirror_obj.pos, mirror_obj.angle, MIRROR_LENGTH),
    .angle = mirror_obj.angle,
    .dir = dir,
    .normal = normal
  };
}

static bool inside_map(struct vec v) {
  return (v.x >= 0 && v.x <= MAP_SIDE - 1 && v.y >= 0 && v.y <= MAP_SIDE - 1);
}

static bool map_segment_intersection(struct segment seg) {
  struct wall *w;

  LIST_FOREACH(w, &walls, next_wall) {
    for(int i=0;i<4;i++) {
      if(segment_segment_intersection(seg, w->segments[i])) {
        return true;
      }
    }
  }

  return false;
}

static float map_ray_intersection(struct ray ray) {
  float t_min = INFINITY;
  struct wall *w;

  int c;
  float t, u;

  LIST_FOREACH(w, &walls, next_wall) {
    for(int i = 0;i < 4; i++) {
      ray_segment_intersection(ray, w->segments[i], &c, &t, &u);
      if((c == 2 || c == 3) && t < t_min && t > EPSILON) {
        t_min = t;
      }
    }
  }

  return t_min;
}

static bool point_in_wall(struct vec v) {
  struct wall *w;
  LIST_FOREACH(w, &walls, next_wall) {
    if(v.x >= w->verts[0].x && v.y <= w->verts[0].y && v.x <= w->verts[2].x && v.y >= w->verts[2].y) {
      return true;
    }
  }

  return false;
}

static bool solution_valid(struct object light, struct mirror mirrors[8]) {
  if(!inside_map(light.pos)) {
    return false;
  }

  if(point_in_wall(light.pos)) {
    return false;
  }

  for(int i = 0; i < 8; i++) {
    struct mirror m1 = mirrors[i];
    if(!inside_map(m1.start)) {
      return false;
    }

    if(!inside_map(m1.end)) {
      return false;
    }

    if(point_in_wall(m1.start)) {
      return false;
    }

    if(point_in_wall(m1.end)) {
      return false;
    }

    if(map_segment_intersection(m1.seg)) {
      return false;
    }

    for(int j = i+1; j < 8; j++) {
      struct mirror m2 =  mirrors[j];
      if(segment_segment_intersection(m1.seg, m2.seg)) {
        return false;
      }
    }
  }

  return true;
}

bool next_hitpoint(struct ray ray, struct mirror mirrors[8], int last_mirror, struct mirror *hit_mirror, struct vec *hitpoint) {
  float t_mirror = INFINITY;
  int c;
  float t, u;
  bool result = true;
  for(int mirror_j = 0; mirror_j < last_mirror; mirror_j++) {
    ray_segment_intersection(ray, mirrors[mirror_j].seg, &c, &t, &u);
    if((c == 2 || c == 3) && t < t_mirror && t > EPSILON) {
      t_mirror = t;
      *hit_mirror = mirrors[mirror_j];
      result = false;
    }
  }

  float t_map = map_ray_intersection(ray);
  t = MIN(t_mirror, t_map);
  *hitpoint = vec_add(ray.start, vec_mul(ray.dir, t));
  return result;
}

struct hitpoint {
  struct vec point;
  LIST_ENTRY(hitpoint) next;
};
LIST_HEAD(score_vert_list, hitpoint);

void add_score_points(struct ray ray, struct vec ray_normals[2], struct vec hitpoint, struct hitpoint **score_point, struct score_vert_list *score_points, polygon_vec_t *score_polygon) {
  struct vec endpoints[2] = { 
    vec_sub(ray.start, vec_mul(ray.dir, 0.5)), 
    vec_add(hitpoint, vec_mul(ray.dir, 0.5)) 
  };
  polygon_t rect = polygon_new();
  for(int i = 0; i < 2; i++) {
    for(int j = 0; j < 2; j++) {
      struct vec score_point_vec = vec_add(endpoints[i ^ j], vec_mul(ray_normals[i], 2));
      if(score_point != NULL) {
        *score_point = (struct hitpoint *) malloc(sizeof(struct hitpoint));
        (*score_point)->point = score_point_vec;
        LIST_INSERT(score_points, *score_point, next);
      }

      polygon_add_point(rect, score_point_vec);
    }
  }

  *score_polygon = polygon_union_rect(*score_polygon, rect);
  polygon_free(rect);
}

static bool raytrace(struct object light_obj, struct object mirror_objs[8], struct mirror mirrors[8], struct score_arg *arg, polygon_vec_t *score_polygon) { 
  
  LIST_HEAD(hitpoint_list, hitpoint) hitpoints = LIST_HEAD_INIT();
  struct score_vert_list score_points = LIST_HEAD_INIT();

  struct ray ray = {
    .start = light_obj.pos,
    .dir = { cosf(light_obj.angle), sinf(light_obj.angle) }
  };
  struct vec ray_normals[2];
  ray_get_normals(&ray, ray_normals, 0.5);

  struct hitpoint *cur_hitpoint, *score_point;
  if(arg != NULL) {
    cur_hitpoint = (struct hitpoint *) malloc(sizeof(struct hitpoint));
    cur_hitpoint->point = light_obj.pos;
    LIST_INSERT(&hitpoints, cur_hitpoint, next);
  }

  struct vec hitpoint;
  for(int mirror_i = 0; mirror_i < 8; mirror_i++) {
    int cnt = 0;
    while(true) {
      cnt++;
      if(cnt > LOOP_ITER_THRESHOLD) {
        //printf("stuck in the first loop, returning!\n");
        return -1;
      }

      struct mirror hit_mirror;

      bool hit_map = next_hitpoint(ray, mirrors, mirror_i, &hit_mirror, &hitpoint);
      if(!hit_map) {
        ray.start = hitpoint;
        ray.dir = vec_sub(ray.dir, vec_mul(hit_mirror.normal, 2 * vec_dot(ray.dir, hit_mirror.normal)));
        ray_get_normals(&ray, ray_normals, 0.5);

        // if(arg != NULL) {
        //   cur_hitpoint = (struct hitpoint *) malloc(sizeof(struct hitpoint));
        //   cur_hitpoint->point = hitpoint;
        //   LIST_INSERT(&hitpoints, cur_hitpoint, next);
        // }
        // add_score_points(ray, ray_normals, hitpoint, &score_point, &score_points, score_polygon);
        
        continue;
      }

      break;
    }

    struct object next_mirror_params = mirror_objs[mirror_i];
    float t1, t2, angle;
    t1 = next_mirror_params.pos.x;
    t2 = next_mirror_params.pos.y;
    angle = next_mirror_params.angle;

    struct object next_mirror;
    struct vec mirror_start_position = vec_add(ray.start, vec_mul(vec_sub(hitpoint, ray.start), t1));
    next_mirror.pos = mirror_start_position;
    next_mirror.angle = angle;
    preprocess_mirror(next_mirror, &mirrors[mirror_i]);
    
    next_mirror.pos = vec_sub(next_mirror.pos, vec_mul(mirrors[mirror_i].seg.dir, t2));
    if(!inside_map(next_mirror.pos)) {
      return -1;
    }
    preprocess_mirror(next_mirror, &mirrors[mirror_i]);

    ray.start = mirror_start_position;
    ray.dir = vec_sub(ray.dir, vec_mul(mirrors[mirror_i].normal, 2 * vec_dot(ray.dir, mirrors[mirror_i].normal)));
    ray_get_normals(&ray, ray_normals, 0.5);
  

    // if(arg != NULL) {
    //   cur_hitpoint = (struct hitpoint *) malloc(sizeof(struct hitpoint));
    //   cur_hitpoint->point = ray.start;
    //   LIST_INSERT(&hitpoints, cur_hitpoint, next);
    // }
  }

  if(!solution_valid(light_obj, mirrors)) {
    return false;
  }

  ray = (struct ray) {
    .start = light_obj.pos,
    .dir = { cosf(light_obj.angle), sinf(light_obj.angle) }
  };
  ray_get_normals(&ray, ray_normals, 0.5);
  int cnt = 0;
  while(true) {
    cnt++;
    if(cnt > LOOP_ITER_THRESHOLD) {
      //printf("stuck in the second loop, returning!\n");
      return -1;
    }

    if(cnt == 10) {
      //break;
    }

    struct mirror hit_mirror;

    bool hit_map = next_hitpoint(ray, mirrors, 8, &hit_mirror, &hitpoint);
    if(arg != NULL) {
      cur_hitpoint = (struct hitpoint *) malloc(sizeof(struct hitpoint));
      cur_hitpoint->point = hitpoint;
      LIST_INSERT(&hitpoints, cur_hitpoint, next);
    }

    add_score_points(ray, ray_normals, hitpoint, &score_point, &score_points, score_polygon);

    if(!hit_map) {
      ray.start = hitpoint;
      ray.dir = vec_sub(ray.dir, vec_mul(hit_mirror.normal, 2 * vec_dot(ray.dir, hit_mirror.normal)));
      ray_get_normals(&ray, ray_normals, 0.5);
      continue;
    }

    break;
  }

  if(arg != NULL) {
    uint32_t cnt = LIST_SIZE(&hitpoints); 
    arg->path_len = cnt;
    arg->path = (struct vec *) malloc(sizeof(struct vec) * cnt);
    int i = 0;
    struct hitpoint *hp;
    LIST_FOREACH(hp, &hitpoints, next) {
      arg->path[i] = hp->point;
      i++;
    }

    cnt = LIST_SIZE(&score_points);
    arg->score_rects_len = cnt;
    arg->score_rects = (struct vec *) malloc(sizeof(struct vec) * cnt);
    i = 0;
    LIST_FOREACH(hp, &score_points, next) {
      arg->score_rects[i] = hp->point;
      i++;
    }
  }

  return true;
}

float score_solution(struct object light, struct object mirror_objs[8], struct mirror mirror_result[8], struct score_arg *arg) {
  polygon_vec_t score_polygon = NULL;
  bool valid = raytrace(light, mirror_objs, mirror_result, arg, &score_polygon);

  if(!valid || score_polygon == NULL) {
    return -1;
  }
  score_polygon = polygon_clip_walls(score_polygon);

  if(arg != NULL) {
    polygon_to_points(score_polygon, &arg->clipped_polygon, &arg->clipped_polygon_size);
  }

  float area = polygon_area(score_polygon);

  polygon_free(score_polygon);
  
  return area/FREE_SPACE_AREA;
}

void score_arg_free(struct score_arg *arg) {
  if(arg == NULL) {
    return;
  }
  free(arg->path);
  free(arg->score_rects);
  free(arg->clipped_polygon);
}