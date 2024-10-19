from birds import *
from demo_function import *
from tqdm import *
import numpy as np
from numpy.linalg import norm
import time
from model_module import *
from model import score_solution

global restart_velocity
global restart_position
restart_position  = 0
restart_velocity = 0
class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.best_position = position
        self.best_value = f(position)
        self.global_best_position = position
        self.global_best_value = self.best_value

class Bird:
    def __init__(self, x, y, alpha, velocity):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.velocity = velocity
        self.best_position = np.array([x,y,alpha])
        self.position = np.array([self.x, self.y, self.alpha])
        #self.best_value
        #self.global_best_position = np.array([x,y,alpha])
        #self.global_best_value = self.best_value

    def getPosition(self):
        return self.position
    
    def addToPopulation(self):
        population.add(self.getPosition())

    def normalize(self):
        self.x /= 20
        self.y /= 20
        self.alpha /= pi

    def denormalize(self):
        self.x *= 20
        self.y *= 20
        self.alpha *= pi

class Population():

    def __init__(self, position, value):
        self.best_position = position
        self.best_value = value

#best_values_per_population = [Population(np.array([0,0,0]) , 0) for _ in range(9)]
global_best_position = [np.array([np.random.uniform(0, 20), np.random.uniform(0, 20), np.random.uniform(0, pi)]) for _ in range(9)]
#print(global_best_position)
global_best_value = score_solution(global_best_position)
start_time = time.time()

def gpso(num_particles, max_iterations, dimensions=3, checkpoint=1000, hours=6):
    global restart_velocity
    global restart_position
    # Initialize particles
    best_values_per_population = [Population(np.array(np.array([0,0,0]) for _ in range(9)) , 0) for _ in range(num_particles)]
    populations = []
    for _ in range(num_particles):
        population = set()
        while(len(population) < 9):
            bird = Bird(np.random.uniform(0, 20), np.random.uniform(0, 20), np.random.uniform(0, pi), np.random.uniform(-0.1, 0.1, dimensions))
            #bird.addToPopulation()
            population.add(bird)
        population = list(population)
        populations.append(population)
    #particles = [Particle(np.random.uniform(-10, 10, dimensions), np.random.uniform(-3, 3, dimensions)) for _ in range(num_particles)]

    # Global best position and value
    #global_best_position = min(birds, key=lambda p: p.best_value).best_position
    #global_best_value = f(global_best_position)
    
    
    w = 1 
    c1 = 0.5  
    c2 = 0.5 
    gregarious_factor = 0.25  
    v_max = 5
    v_min = 0
    epsilon = 1e-3
    #gamma = 0
    gamma_min = 2
    gamma_max = 4
    delta = 0.25

    u = np.array([1,1,1])
    l = np.array([0,0,0])

    it = 0

    #for iteration in tqdm(range(max_iterations)):
    while(time.time()-start_time < 3600*hours):
        cnt = 0
        for p in populations:
            cntt = 0
            for bird in p:

                bird.normalize()
                #bird.position = np.array(bird.position)
                #print(particle.velocity)
                # Update particle velocity
                #print(bird)
                #print(bird.best_position)
                #print(bird.position)
                r1, r2 = np.random.rand(1), np.random.rand(1)
                cognitive_velocity = c1 * r1 * np.subtract(populations[cnt][cntt].best_position, bird.position)
                #social_velocity = c2 * r2 * np.subtract(global_best_position[cntt], bird.position)
                gregarious_velocity = gregarious_factor * np.subtract(np.mean([g.position for g in p], axis=0), bird.position)
                
                '''particle.velocity = (w * particle.velocity +
                                    cognitive_velocity +
                                    social_velocity +
                                    gregarious_velocity)
                '''
                
                #print(particle.velocity)
                #print(norm((particle.position - global_best_position),2))
                # or norm(particle.velocity, 2) < epsilon
                if norm(bird.velocity, 2) < epsilon:
                    #print(True)
                    bird.velocity = np.random.uniform(-0.03,0.03, dimensions)
                    restart_velocity +=1
                else:
                    #particle.velocity = particle.gamma * random.random() * (particle.position -  global_best_position)
                    bird.velocity = (w * bird.velocity +
                                    cognitive_velocity +
                                    #social_velocity)
                                    gregarious_velocity)
                #print(particle.velocity)
                    


                #particle.velocity = min(v_max, particle.velocity)
                #particle.velocity = max(v_min, particle.velocity)
                bird.velocity = np.clip(bird.velocity, -0.1, 0.1)

                #print(particle.position -  global_best_position)
                #particle.velocity[:dimensions] = np.c
                
                # Update particle position
                #print(norm((abs(particle.position) - [3,3,3]),2))
                #print((particle.velocity))
                if norm(np.subtract(abs(bird.position), l),2) > epsilon and norm(np.subtract(abs(bird.position), u),2) > epsilon:
                    bird.position += bird.velocity

                else:
                    restart_position += 1
                    bird.position = np.random.uniform(0, 1, dimensions)
                
                # Keep position within bounds
                bird.position = np.clip(bird.position, 0, 1)
                
                # Evaluate new position

                bird.denormalize()
                #bird.position = tuple(bird.position)
                cntt+=1

            positions = [map(lambda bird: bird.position, p)]
            print(positions)
            current_value = score_solution(positions)
            #print(current_value)
            if current_value > best_values_per_population[cnt].best_value:
                best_values_per_population[cnt].best_value = current_value
                best_values_per_population[cnt].best_position = positions

                for i in range(9):
                    populations[cnt][cntt].best_position = best_values_per_population[cnt].best_position[cntt]
        
            
            #print(particle.position)    
        # Update global best position
        current_global_best = min(best_values_per_population, key=lambda p: p.best_value)
        if current_global_best.best_value > global_best_value:
            global_best_value = current_global_best.best_value
            global_best_position = current_global_best.best_position
        cnt +=1

        
        if it%checkpoint == 0:
            print(f"Iteration {it + 1}/{max_iterations}, Global Best Value: {global_best_value}")

            file = open("checkpoints.txt", "a")
            file.write(f"Iteration {it + 1}/{max_iterations}, Global Best Value: {global_best_value}, Global Best Position: {global_best_position}\n")
            file.write("###############################################################")
            file.close()

        it+=1

    return global_best_position, global_best_value

num_particles = 2
#dimensions = 27
max_iterations = 100000
best_position, best_value = gpso(num_particles, max_iterations)
end_time = time.time()
print("Best Position:", best_position)
print("Best Value:", best_value)
print(f"Vrijeme izvođenja je {end_time-start_time} sekundi")
print(restart_position, restart_velocity)
