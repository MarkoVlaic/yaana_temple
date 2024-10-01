from tkinter import *
from tkinter import ttk

from model_module.model import *

if __name__ == '__main__':
  model_init()
  (walls, size) = get_walls()
  
  CANV_W = 500
  CANV_H = 500
  MAP_W = 20
  MAP_H = 20

  top = Tk()
  C = Canvas(top, bg='white', height=CANV_W, width=CANV_H)

  for wall in walls:
    y = 20 - wall.y
    cx = (wall.x/MAP_W) * CANV_W
    cy = (y/MAP_H) * CANV_H
    cw = (wall.w/MAP_W) * CANV_W
    ch = (wall.h/MAP_H) * CANV_H

    print(f'draw {wall.x} {wall.y} {wall.w} {wall.h} | {cx} {cy} {cw} {ch}')

    C.create_rectangle(cx, cy, cx + cw, cy + ch, fill='black', outline='black')

  C.pack()
  top.mainloop()