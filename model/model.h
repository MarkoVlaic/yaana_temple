#ifndef YAANA_MODEL_H
#define YAANA_MODEL_H

#include "list.h"
#include "geom.h"
#include "model_data.h"

void model_init();
void get_walls(struct wall **wa, uint32_t *cnt);
float score_solution(struct object light, struct object mirror_objs[8], struct mirror mirror_result[8], struct score_arg *arg);
void score_arg_free(struct score_arg *arg);

#endif