from birds import *
from demo_function import *
from tqdm import *
import numpy as np
from numpy.linalg import norm
import time
from model_module import *
from model import score_solution

restart_position  = 0
restart_velocity = 0

class Bird:
    def __init__(self, x, y, alpha, velocity):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.velocity = velocity
        self.best_position = np.array([x,y,alpha])
        self.position = np.array([self.x, self.y, self.alpha])

    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        self.position = position

    def setBestPosition(self, position):
        self.best_position = position
    
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

    def checkPosition(self, epsilon): #provjerava da nisu sve tri vrijednosti objekta (x,y,alpha) zapele u epsilon okolinu (0,0,0) ili (1,1,1)
        res = 0

        x,y,alpha = self.position[0], self.position[1], self.position[2]

        if(1-epsilon-x) > 0 and (x > epsilon):
            res +=1
        
        if(1-epsilon-y) > 0 and (y > epsilon):
            res +=1

        if(1-epsilon-alpha) > 0 and (alpha > epsilon):
            res +=1

        return res > 1
        
        

class Population(): #klasa u kojoj pratim najbolju poziciju i najbolju vrijednost za svaku populaciju, populacija = lampa + 8 ogledala

    def __init__(self, position, value):
        self.best_position = position
        self.best_value = value

global_best_position = [np.array([np.random.uniform(0, 20), np.random.uniform(0, 20), np.random.uniform(0, pi)]) for _ in range(9)]
#global_best_value = random.random()
global_best_value = score_solution(global_best_position) 
start_time = time.time()

def gpso(num_particles, max_iterations, dimensions=3, checkpoint=1000, hours=6):
    global restart_velocity
    global restart_position
    global global_best_value
    global global_best_position

    #stvaranje ptica i populacija
    best_values_per_population = [Population(np.array(np.array([0,0,0]) for _ in range(9)) , 0) for _ in range(num_particles)] 
    populations = []
    for _ in range(num_particles):
        population = set()
        while(len(population) < 9):
            bird = Bird(np.random.uniform(0, 20), np.random.uniform(0, 20), np.random.uniform(0, pi), np.random.uniform(-0.01, 0.01, dimensions))
            population.add(bird)

        population = list(population)
        populations.append(population)
    
    
    w = 1 # težina kojom se množi trenutni velocity za svaki objekt
    c1 = 0.05  # c1, c2 su faktori kojima se množe cognitive i social težine
    c2 = 0.05 
    gregarious_factor = 2.5*1e-4  #faktor kojim se množi gregarious težina 
    epsilon = 1e-3 # za definiciju epsilon okoline

    it = 0

    #for iteration in tqdm(range(max_iterations)):
    while(time.time()-start_time < 3600*hours):
        cnt = 0
        for p in populations: # idi za svaku populaciju
            cntt = 0
            for bird in p: # idi za svaki objekt u populaciji

                bird.normalize() #normaliziraj objekt
                
                #r1 i r2 su faktori koji unose nasumičnost u odabir težina, sljedeće linije izračunavaju težine
                r1, r2 = np.random.uniform(0, 0.5), np.random.uniform(0, 0.5)
                cognitive_velocity = c1 * r1 * np.subtract(populations[cnt][cntt].best_position, bird.position)
                social_velocity = c2 * r2 * np.subtract(global_best_position[cntt], bird.position)
                gregarious_velocity = gregarious_factor * np.subtract(np.mean([g.position for g in p], axis=0), bird.position)
                
                #provjeri je li velocity u epsilon okolini (0,0,0), ako je generiraj ga ponovno, ako nije izračunaj ga po formuli dolje
                if norm(bird.velocity, 2) < epsilon:
                    bird.velocity = np.random.uniform(-0.01,0.01, dimensions) 
                    restart_velocity +=1
                else:  
                    bird.velocity = (w * bird.velocity +
                                    cognitive_velocity +
                                    social_velocity + 
                                    gregarious_velocity)
                
                np.clip(bird.velocity, -0.01, 0.01, out=bird.velocity) #ograniči velocity na interval (-0.1, 0.1)

                '''opis funkcije checkPosition gore u klasi, ako vrati true, dodaj velocity na trenutnu poziciju objekta, inače generiraj
                novi poziciju objekta'''

                if bird.checkPosition(epsilon): 
                    tmp = np.add(bird.position, bird.velocity)
                    bird.setPosition(tmp)
                    
                else:
                    restart_position += 1
                    bird.setPosition(np.random.uniform(0, 1, dimensions))
                
                
                np.clip(bird.position, 0, 1, out=bird.position)#ograniči poziciju objekta na interval (0,1)
                #bird.setPosition(tmp)
                

                bird.denormalize() #denormaliziraj objekt
                cntt+=1

            '''linija ispod stvara listu pozicija objekata koje ćemo predati funkciji score_solution, dogovorili smo se da ne 
            predajemo objekte klase nego pozicije
            '''
            positions = list(g.position for g in p) 
            
            #current_value = random.random()
            current_value = score_solution(positions) #izračunaj score

            '''provjeri je li score za populaciju bolji od trenutnog najboljeg, ako je postavi tu vrijednost kao najbolju za tu
            populaciju i postavi tu poziciju objekata kao novu najbolju poziciju objekata'''

            if current_value > best_values_per_population[cnt].best_value:
                best_values_per_population[cnt].best_value = current_value
                best_values_per_population[cnt].best_position = positions

                for i in range(9): #potrebno za cognitive velocity
                    populations[cnt][i].setBestPosition(best_values_per_population[cnt].best_position[i])
        
            
            cnt +=1
            
        current_global_best = max(best_values_per_population, key=lambda p: p.best_value) #vraća objekt koji ima najbolju vrijednost scorea od svih populacija
        
        '''provjerava je li trenutno izračunati current_global_best bolji od dosad najboljeg scorea, 
        ako je, postavi tu vrijednost kao najbolju i postavi te pozicije objekata kao najbolje'''
        if current_global_best.best_value > global_best_value:
            global_best_value = current_global_best.best_value
            global_best_position = current_global_best.best_position

        
        if it%checkpoint == 0:
            print(f"Iteration {it + 1}/{max_iterations}, Global Best Value: {global_best_value}")

            #za zapis checkpointa
            '''
            file = open("checkpoints.txt", "a")
            file.write(f"Iteration {it + 1}/{max_iterations}, Global Best Value: {global_best_value}, Global Best Position: {global_best_position}\n")
            file.write("###############################################################")
            file.close()
            '''
        it+=1

    return global_best_position, global_best_value 

num_particles = 35 #broj populacija koje stvaramo
#dimensions = 27
max_iterations = 100000
best_position, best_value = gpso(num_particles, max_iterations)
end_time = time.time()
print("Best Position:", best_position)
print("Best Value:", best_value)
print(f"Vrijeme izvođenja je {end_time-start_time} sekundi")
#print(restart_position, restart_velocity)
