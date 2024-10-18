from _model import lib, ffi

class ScoreResult:
  def __init__(self, score, arg):
    self.score = score
    self.arg = arg

    if self.arg == ffi.NULL:
      return

    self.path = []
    for i in range(arg.path_len):
      self.path.append(arg.path[i])

    self.score_rects = []
    for i in range(arg.score_rects_len):
      self.score_rects.append(arg.score_rects[i])

    self.clipped_polygon = []
    for i in range(arg.clipped_polygon_size):
      self.clipped_polygon.append(arg.clipped_polygon[i])

  def get_score(self):
    return self.score

  def get_mirrors(self):
    return self.arg.mirrors

  def get_path(self):
    return self.path

  def get_score_rects(self):
    return self.score_rects

  def get_clipped_polygon(self):
    return self.clipped_polygon

  def free(self):
    pass
    #ffi.score_arg_free(self.arg)

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

def evaluate_solution(objs, collect_arg=True):
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

  arg = ffi.new('struct score_arg *')
  if not collect_arg:
    arg = ffi.NULL


  score = lib.score_solution(light_obj[0], mirror_objs, arg)
  return ScoreResult(score, arg)

def score_solution(objs):
  result = evaluate_solution(objs, False)
  return result.get_score()