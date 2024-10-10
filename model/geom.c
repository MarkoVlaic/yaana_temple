#include <stdbool.h>
#include <math.h>

#include "geom.h"

struct vec vec_add(struct vec v1, struct vec v2) {
  struct vec result = {
    .x = v1.x + v2.x,
    .y = v1.y + v2.y
  };

  return result;
}

struct vec vec_mul(struct vec v1, float f) {
  struct vec result = {
    .x = v1.x * f,
    .y = v1.y * f
  };

  return result;
}

// v1 - v2
struct vec vec_sub(struct vec v1, struct vec v2) {
  struct vec result = {
    .x = v1.x - v2.x,
    .y = v1.y - v2.y
  };

  return result;
}

float vec_dot(struct vec v1, struct vec v2) {
  return v1.x * v2.x + v1.y * v2.y;
}

static float vec_cross(struct vec v1, struct vec v2) {
  return v1.x * v2.y - v1.y * v2.x;
}

struct segment segment_new(struct vec pos, float angle, float length) {
  struct segment result = {
    .start = pos,
    .dir = vec_mul((struct vec) { cosf(angle), sinf(angle) }, length)
  };

  return result;
}

void ray_ray_intersection(struct ray ray1, struct ray ray2, int *c, float *t1, float *t2) {
  float rs = vec_cross(ray1.dir, ray2.dir);
  float qpr = vec_cross(vec_sub(ray2.start, ray1.start), ray1.dir);

  // CASE 1 - rays are collinear and maybe overlap
  if(rs == 0 && qpr == 0) {
    *c = 1;
    *t1 = vec_dot(vec_sub(ray2.start, ray1.start), ray1.dir) / vec_dot(ray1.dir, ray1.dir);
    *t2 = vec_dot(vec_sub(vec_add(ray2.start, ray2.dir), ray1.start), ray1.dir) / vec_dot(ray1.dir, ray1.dir);
    return;
  }

  // CASE 2 - rays are parallel so they don't intersect
  if(rs == 0 && qpr != 0) {
    *c = 2;
    *t1 = 0;
    *t2 = 0;
    return;
  }

  float qps = vec_cross(vec_sub(ray2.start, ray1.start), ray2.dir);
  float t = qps / rs;
  float u = qpr / rs;

  if(rs != 0 && t >= 0 && u >= 0) {
    *c = 3;
    *t1 = t;
    *t2 = u;
    return;
  }

  *c = 4;
  *t1 = 0;
  *t2 = 0;
}

void ray_segment_intersection(struct ray ray, struct segment seg, int *c, float *t1, float *t2) {
  int rr_case;
  float t, u;

  ray_ray_intersection(ray, (struct ray) { seg.start, seg.dir }, &rr_case, &t, &u);

  if(rr_case == 1 && t < 0 && u < 0) {
    *c = 1;
    *t1 = 0;
    *t2 = 0;
    return;
  }

  if(rr_case == 2) {
    *c = 1;
    *t1 = 0;
    *t2 = 0;
    return;
  }

  if(rr_case == 3 && (t <= 0 || u < 0 || u > 1)) {
    *c = 1;
    *t1 = 0;
    *t2 = 0;
    return;
  }

  if(rr_case == 4) {
    *c = 1;
    *t1 = 0;
    *t2 = 0;
    return;
  }

  if(rr_case == 1) {
    if(t > 0 && u >= 0) {
      *c = 2;
      *t1 = MIN(t, u);
      *t2 = 0;
      return;
    }

    if(t >= 0) {
      *c = 2;
      *t1 = t;
      *t2 = 0;
      return;
    }
    
    if(u >= 0) {
      *c = 2;
      *t1 = 0;
      *t2 = 0;
      return;
    }
  }

  *c  = 3;
  *t1 = t;
  *t2 = u;
}

bool segment_segment_intersection(struct segment seg1, struct segment seg2) {
  int c;
  float t, u;
  ray_ray_intersection((struct ray) { seg1.start, seg1.dir }, (struct ray) { seg2.start, seg2.dir }, &c, &t, &u);
  float rs = vec_dot(seg1.dir, seg2.dir);

  if(c == 1 && rs > 0 && t <= u && ((0 <= t && t <= 1) || (0 <= u && u <= 1))) {
    return true;
  }

  if(c == 1 && rs < 0 && t >= u && ((0 <= t && t <= 1) || (0 <= u && u <= 1))) {
    return true;
  }

  if(c == 2) {
    return false;
  }

  if(c == 3 && 0 <= t && t <= 1 && 0 <= u && u <= 1) {
    return true;
  }

  return false;
}

void ray_get_normals(const struct ray *ray, struct vec normals[2], float len) {
  normals[0] = vec_mul((struct vec) { -ray->dir.y, ray->dir.x }, len);
  normals[1] = vec_mul((struct vec) { ray->dir.y, -ray->dir.x }, len);
}