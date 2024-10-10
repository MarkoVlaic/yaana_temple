from tkinter import *
from tkinter import ttk

from model_module.model import *

solution = [
  (5,5,0.26),
  (11.5,6.5,0.9),
  (11.9,16.5,0.95),
  (15.2,17.6,2.45),
  (13.8,12.0,0.92),
  (1.6,6.2,2.53),
  (2.2,14.7,0.66),
  (18,12,1.6),
  (13.8,11.5,-0.54)
]

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

if __name__ == '__main__':
  model_init()
  (walls, size) = get_walls()
  
  top = Tk()
  canvas = Canvas(top, bg='white', height=CANV_W, width=CANV_H)

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

  (score, path, mirrors, score_points) = score_solution(solution)
  print(score)
  print(path)

  light_x = solution[0][0]
  light_y = solution[0][1]
  canvas.create_circle(x_to_canvas(light_x), y_to_canvas(light_y), 5, fill='red')

  for i in range(8):
    mirror = mirrors[i]
    sx = x_to_canvas(mirror.start.x)
    sy = y_to_canvas(mirror.start.y)
    ex = x_to_canvas(mirror.end.x)
    ey = y_to_canvas(mirror.end.y)

    canvas.create_line(sx, sy, ex, ey, fill='red')

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

  for i in range(len(score_points)):
    point = score_points[i]
    canvas.create_circle(x_to_canvas(point.x), y_to_canvas(point.y), 2, fill='red')
  
  for i in range(0, len(score_points), 4):
    points = score_points[i:i+4]
    points[2], points[3] = points[3], points[2]
    canv_points = []
    for point in points:
      canv_points.append(x_to_canvas(point.x))
      canv_points.append(y_to_canvas(point.y))
    print(len(canv_points))
    canvas.create_polygon(canv_points, fill='red')

  canvas.pack()
  top.mainloop()