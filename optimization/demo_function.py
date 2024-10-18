
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import norm

# Define the function
'''
def f(x, y, z):
    return (np.sin(x) * np.cos(y) -
            0.5 * np.exp(-(x**2 + y**2 + z**2)) +
            0.25 * np.sin(3 * z) +
            (x**2 - 1)**2 +
            (y**2 - 1)**2 +
            (z**2 - 1)**2)

def f(x,y,z):
    return x**2 + y**2 + z**2
'''
def f(x):
    
    term1 = np.sum(np.sin(x) + np.cos(2 * x) + np.log(1 + np.exp(x)))
    
    term2 = 0
    for i in range(26):
        for j in range(i + 1, 27):
            term2 += 1 / ((x[i] - x[j]) ** 2 + 1)
    
    return term1 + term2
# Create a grid of points
'''
def f(x):
    return norm(x,2)

x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
z = np.linspace(-3, 3, 50)

X, Y, Z = np.meshgrid(x, y, z)

# Compute the function values
F = f(X, Y, Z)


# Plotting the function
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Choose a slice for visualization
slice_index = 25  # Change this index to view different slices
ax.contourf(X[:, :, slice_index], Y[:, :, slice_index], F[:, :, slice_index], levels=50, cmap='viridis')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('f(x, y, z)')
ax.set_title('Contour Plot of f(x, y, z) at z = {:.2f}'.format(Z[0, 0, slice_index]))

plt.show()
'''