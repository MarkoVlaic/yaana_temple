import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import norm

from demo_function import *

l = [1,2,3]
n = norm(l,2)
#print(n)

l = np.zeros(27)

a = (1,3,0)
b = (2,1,1)

a = np.array(a)
b = np.array(b)
print(list(np.add(a,b)))

c = np.array([1,2,3])
print(tuple(c))