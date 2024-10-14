from model import *
from random import random
from math import pi

def random_tuple():
  a = random() * 20
  b = random() * 20
  c = random() * 2 * pi

  return (a, b, c)

iters = int(1e6)

model_init()

for _ in range(iters):
  configuration = []
  for i in range(9):
    configuration.append(random_tuple())

  #print(configuration)
  score_solution(configuration, False)