#ifndef YAANA_GEOM_H
#define YAANA_GEOM_H

#include <stdbool.h>

#define PI 3.14159265358979323846
#define MIN(X, Y) ((X) < (Y) ? (X) : (Y))

struct vec {
  float x;
  float y;
};

struct object {
  struct vec pos;
  float angle;
};

struct segment {
  struct vec start;
  struct vec dir;
};

struct ray {
  struct vec start;
  struct vec dir;
};

struct vec vec_add(struct vec v1, struct vec v2);
struct vec vec_mul(struct vec v1, float f);
struct vec vec_sub(struct vec v1, struct vec v2);
float vec_dot(struct vec v1, struct vec v2);

struct segment segment_new(struct vec pos, float angle, float length);

void ray_ray_intersection(struct ray ray1, struct ray ray2, int *c, float *t1, float *t2);
void ray_segment_intersection(struct ray ray, struct segment seg, int *c, float *t1, float *t2);
bool segment_segment_intersection(struct segment seg1, struct segment seg2);
void ray_get_normals(const struct ray *ray, struct vec normals[2], float length);

#endif