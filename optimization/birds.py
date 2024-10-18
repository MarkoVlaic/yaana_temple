import random
import math
import normalize
import numpy as np

population = []
pi = math.pi

N = 5
n = 3

def get_bird():
    x = random.random()*20
    y = random.random()*20
    alpha = random.random()*pi
    velocity = list(np.random.uniform(-0.1, 0.1, n))


    return x,y,alpha, velocity

def main():
    velocities = []
    for _ in range(N):
        birds = set()
        while(len(birds) < n):
            x,y,alpha, velocity = get_bird()
            velocities.append(velocity)
            birds.add((x,y,alpha))
        birds = list(birds)
        
        population.append(list(birds))

if __name__ == "__main__":
    main()
    population = list(population)
    print(population)

    birds = normalize.normalize(population)
    print(birds)

    birds = normalize.denormalize(birds)
    print(birds)