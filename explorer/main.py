from tkinter import *
from tkinter import ttk
from random import random
from math import pi
from numpy import array
import numpy as np

from model_module.model import *

class State:
  def __init__(self):
    self.walls = []

  def set_walls(self, walls):
    self.walls = walls

  def get_walls(self):
    return self.walls

  def set_light(self, light):
    self.light = light

  def get_light(self):
    return self.light

  def set_mirrors(self, mirrors):
    self.mirrors = mirrors

  def get_mirrors(self):
    return self.mirrors

  def set_path(self, path):
    self.path = path
  
  def get_path(self):
    return self.path

  def set_score_rects(self, sr):
    self.score_rects = sr

  def get_score_rects(self):

    return self.score_rects
  def set_clipped_polygon(self, cp):
    self.clipped_polygon = cp

  def get_clipped_polygon(self):
    return self.clipped_polygon

class Layer:
  def __init__(self, name, draw_fn, enabled=True):
    self.name = name
    self.draw_fn = draw_fn
    self.enabled = BooleanVar(value=enabled)


# solution = [
#   (5,5,0.26),
#   (11.5,6.5,0.9),
#   (11.9,16.5,0.95),
#   (15.2,17.6,2.45),
#   (13.8,12.0,0.92),
#   (1.6,6.2,2.53),
#   (2.2,14.7,0.66),
#   (18,12,1.6),
#   (13.8,11.5,-0.54)
# ]

# solution = [
#   (5, 5, 0.26),
#   (0.5, random(), random() * pi),
#   (0.5, random(), random() * pi),
#   (0.5, random(), random() * pi),
#   (0.5, random(), random() * pi),
#   (0.5, random(), random() * pi),
#   (0.5, random(), random() * pi),
#   (0.5, random(), random() * pi),
#   (0.5, random(), random() * pi)
# ]

solution = [(np.float64(3.289805735716872), np.float64(2.856901780893477), np.float64(0.4596867684418661)), (6.570567607879639, 16.517671585083008, 1.337201714515686), (6.446788787841797, 16.790802001953125, 0.7311407923698425), (6.302221298217773, 16.661163330078125, 0.840877890586853), (6.120842933654785, 16.36044692993164, 1.1364237070083618), (6.101320266723633, 16.05536651611328, 1.5072717666625977), (5.883703708648682, 15.854426383972168, 0.975968062877655), (6.7842206954956055, 16.7899227142334, 2.6493875980377197), (6.384472370147705, 16.45948028564453, 2.062851667404175)]


# solution = [
#   (5, 5, 0.26),
#   (11.5, 6.5, 0.9),
#   (11.9, 16.5, 0.95),
#   (15.2, 17.6, 2.45),
#   (13.8, 12.0, 0.92),
#   (1.6, 6.2, 2.53),
#   (2.2, 14.7, 0.7),
#   (8.5, 14.2, 2.325),
#   (8.7, 3.05, 2.525)
# ]

# solution = [
#   (5,5,0.26),
#   (11.5,6.5,0.9),
#   (11.9,16.5,0.95),
#   (15.2,17.6,2.45),
#   (13.8,12.0,0.92),
#   (1.6,6.2,2.53),
#   (2.2,14.7,0.7),
#   (8.5,14.2,2.325),
#   (8.7,3.05,2.525)
# ]

CANV_W = 800
CANV_H = 800
MAP_W = 20
MAP_H = 20

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def y_to_canvas(map_y):
  return ((MAP_H - map_y)/MAP_H) * CANV_H

def x_to_canvas(map_x):
  return (map_x/MAP_W) * CANV_W 

def h_to_canvas(map_h):
  return (map_h/MAP_H) * CANV_H

def w_to_canvas(map_w):
  return x_to_canvas(map_w)

def draw_walls(state, canvas):
  walls = state.get_walls()
  for wall in walls:
    cx = x_to_canvas(wall.pos.x)
    cy = y_to_canvas(wall.pos.y)
    cw = w_to_canvas(wall.w)
    ch = h_to_canvas(wall.h)

    print(f'draw {wall.pos.x} {wall.pos.y} {wall.w} {wall.h} | {cx} {cy} {cw} {ch}')
    canvas.create_rectangle(cx, cy, cx + cw, cy + ch, fill='black', outline='black')

    for i in range(4):
      seg = wall.segments[i]
      start = seg.start
      end = (seg.start.x + seg.dir.x, seg.start.y + seg.dir.y)

      sx = x_to_canvas(start.x)
      sy = y_to_canvas(start.y)
      ex = x_to_canvas(end[0])
      ey = y_to_canvas(end[1])

      canvas.create_line(sx, sy, ex, ey, fill='red')

def draw_light(state, canvas):
  light = state.get_light()
  light_x = light[0]
  light_y = light[1]
  canvas.create_circle(x_to_canvas(light_x), y_to_canvas(light_y), 5, fill='red')

def draw_mirrors(state, canvas):
  mirrors = state.get_mirrors()

  for i in range(8):
    mirror = mirrors[i]
    sx = x_to_canvas(mirror.start.x)
    sy = y_to_canvas(mirror.start.y)
    ex = x_to_canvas(mirror.end.x)
    ey = y_to_canvas(mirror.end.y)

    print('draw mirror')
    print(f'map ({mirrors[i].start.x}, {mirrors[i].start.y}) - ({mirrors[i].end.x}, {mirrors[i].end.y})')
    print(f'canvas ({sx}, {sy}) - ({ex}, {ey})')

    canvas.create_line(sx, sy, ex, ey, fill='red')

def draw_path(state, canvas):
  path = state.get_path()
  for i in range(len(path) - 1):
    start = path[i]
    end = path[i+1]

    sx = x_to_canvas(start.x)
    sy = y_to_canvas(start.y)
    ex = x_to_canvas(end.x)
    ey = y_to_canvas(end.y)
    
    print(f'draw map ({start.x}, {start.y}) - ({end.x}, {end.y})')
    #print(f'draw canvas ({sx}, {sy}) - ({ex}, {ey})')

    canvas.create_line(sx, sy, ex, ey, fill='blue')

def draw_score_rects(state, canvas):
  score_rects = state.get_score_rects()
  for i in range(len(score_rects)):
    point = score_rects[i]
    canvas.create_circle(x_to_canvas(point.x), y_to_canvas(point.y), 2, fill='red')
  
  for i in range(0, len(score_rects), 4):
    points = score_rects[i:i+4]
    canv_points = []
    for point in points:
      canv_points.append(x_to_canvas(point.x))
      canv_points.append(y_to_canvas(point.y))
    print(len(canv_points))
    canvas.create_polygon(canv_points, fill='red')

def draw_clipped_polygon(state, canvas):
  clipped_polygon = state.get_clipped_polygon()
  canv_points = []
  for i in range(len(clipped_polygon)):
    point = clipped_polygon[i]
    canv_points.append(x_to_canvas(point.x))
    canv_points.append(y_to_canvas(point.y))
    canvas.create_circle(x_to_canvas(point.x), y_to_canvas(point.y), 3, fill='orange')

  canvas.create_polygon(canv_points, fill='orange')

def create_layers():
  layers = [
    Layer('walls', draw_walls),
    Layer('light', draw_light),
    Layer('mirrors', draw_mirrors),
    Layer('path', draw_path),
    Layer('score rects', draw_score_rects),
    Layer('clipped polygon', draw_clipped_polygon, False)
  ]

  return layers

def draw_layers(layers, state, canvas):
  canvas.create_rectangle(0, 0 , CANV_W, CANV_H, fill='white')
  for layer in layers:
    print(f'layer {layer.name} enabled {layer.enabled}')
    if layer.enabled.get():
      layer.draw_fn(state, canvas)

if __name__ == '__main__':
  model_init()
  (walls, size) = get_walls()
  score_result = evaluate_solution(solution)
  print(f'got score: {score_result.get_score()}')
  print('api: ', score_solution(solution))
  mirrors = score_result.get_mirrors()

  print('mirrors:')
  for mirror in mirrors:
    print(f'({mirror.start.x} {mirror.start.y} {mirror.angle})')

  state = State()
  state.set_walls(walls)
  state.set_light(solution[0])
  state.set_path(score_result.get_path())
  state.set_mirrors(score_result.get_mirrors())
  state.set_score_rects(score_result.get_score_rects())
  state.set_clipped_polygon(score_result.get_clipped_polygon())

  top = Tk()
  canvas = Canvas(top, bg='white', height=CANV_W, width=CANV_H)
  canvas.pack()

  layers = create_layers()
  layer_toggles_frame = ttk.Frame(top)

  layer_toggles_frame.pack()

  for (i, layer) in enumerate(layers):
    toggle = ttk.Checkbutton(layer_toggles_frame, text=layer.name, variable=layer.enabled, onvalue=True, offvalue=False, command=lambda: draw_layers(layers, state, canvas))
    toggle.grid(row=0, column=i)

  draw_layers(layers, state, canvas)

  top.mainloop()