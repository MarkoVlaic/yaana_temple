from _model import lib, ffi

def model_init():
  lib.model_init()

def get_walls():
  walls_p = ffi.new('struct wall **')
  size_p = ffi.new('uint32_t *')

  lib.get_walls(walls_p, size_p)

  size = size_p[0]
  wall_a = walls_p[0]
  walls = []

  for i in range(size):
    walls.append(wall_a[i])
  return (walls, size)

def score_solution(objs):
  light_tuple = objs[0]
  light_obj = ffi.new('struct object *')
  light_obj.pos.x = light_tuple[0]
  light_obj.pos.y = light_tuple[1]
  light_obj.angle = light_tuple[2]

  mirror_objs = ffi.new('struct object[8]')
  for i in range(8):
    mirror_tuple = objs[i+1]
    mirror_objs[i].pos.x = mirror_tuple[0]
    mirror_objs[i].pos.y = mirror_tuple[1]
    mirror_objs[i].angle = mirror_tuple[2]

  path_p = ffi.new('struct vec **')
  size_p = ffi.new('uint32_t *')
  mirror_results = ffi.new('struct mirror[8]')
  score_points_p = ffi.new('struct vec **')
  score_points_len_p = ffi.new('uint32_t *')

  score = lib.score_solution(light_obj[0], mirror_objs, path_p, size_p, mirror_results, score_points_p, score_points_len_p)

  size = size_p[0]
  path_a = path_p[0]
  path = []
  for i in range(size):
    path.append(path_a[i])

  score_points_len = score_points_len_p[0]
  score_points_a = score_points_p[0]
  score_points = []
  for i in range(score_points_len):
    score_points.append(score_points_a[i])

  return (score, path, mirror_results, score_points)
