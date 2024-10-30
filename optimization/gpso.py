from birds import *
from demo_function import *
from tqdm import *
import numpy as np
from numpy.linalg import norm
import time
from model_module.model import *
import math

restart_position  = 0
restart_velocity = 0

class Bird:
    def __init__(self, x, y, alpha, velocity):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.velocity = velocity
        self.best_position = np.array([self.x,self.y,self.alpha])
        self.position = np.array([self.x, self.y, self.alpha])
        self.best_input = np.array([self.x,self.y,self.alpha])

    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        self.position = position

    def setBestPosition(self, position):
        self.best_position = position
    
    def addToPopulation(self):
        population.add(self.getPosition())

    def normalize_lamp(self):
        self.position[0] /= 19
        self.position[1] /= 19
        self.position[2] /= pi

    def denormalize_lamp(self):
        self.position[0] *= 19
        self.position[1] *= 19
        self.position[2] *= pi
        
    def normalize_mirror(self):
        self.position[2] /= pi

    def denormalize_mirror(self):
        self.position[2] *= pi

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

    def __init__(self, position, value, best_input):
        self.best_position = position
        self.best_value = value
        self.best_input = best_input
        
def top_five(d, key, value1, value2, k=5):
    d[key] = [value1, value2]
    sorted_d = dict(sorted(d.items(), reverse=True))
    sorted_d = dict(list(sorted_d.items())[:k])
    
    return sorted_d

model_init()
global_best_input = [np.array([np.random.uniform(1, 19), np.random.uniform(1, 19), np.random.uniform(0, pi)])]
for i in range(8):
    global_best_input.append(np.array([np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, pi)]))
#global_best_value = random.random()
#print(global_best_position)
tmp_res = score_solution(global_best_input)
#print(tmp_res)

global_best = dict()
value = tmp_res[0]
position = tmp_res[1]
global_best = top_five(global_best, value, position, global_best_input)
#global_best_input = [p for p in global_best_position]
#print(global_best_position)
start_time = time.time()

t_x = 0
t_y = 0
t_alpha = 0
total = 0

def getFactor(current_time, total_time):
    if current_time / total_time < 0.2:
        return 0.5
    if current_time / total_time < 0.4:
        return 0.1
    if current_time / total_time < 0.6:
        return 0.025
    if current_time / total_time < 0.8:
        return 0.01
        
    return 0.005
        
        
    
    

def gpso(num_particles, max_iterations, dimensions=3, checkpoint=1000, hours=6, threshold=0.05):
    global restart_velocity
    global restart_position
    global global_best
    global t_x
    global t_y
    global t_alpha
    global total

    print('gpso')

    epsilon = 1e-4
    #stvaranje ptica i populacija
    best_values_per_population = [
        Population(
            np.array(
                np.array([np.random.uniform(0+epsilon, 1-epsilon),
                np.random.uniform(0+epsilon, 1-epsilon),
                np.random.uniform(0+epsilon, pi-epsilon),
                np.random.uniform(0+epsilon, 1-epsilon)]) for _ in range(9)
            ) , 0, []) for _ in range(num_particles)
        ] 
    populations = []
    #for _ in range(num_particles):
    while(len(populations) < num_particles): #radi ovo sve dok ne stvoris num_particles populacija
        population = list() #stvori set, pa u njega dodaj lampu i onda osam ogledala
        lamp_position = random_lamp()
        population.append(Bird(lamp_position[0], lamp_position[1], np.random.uniform(0+epsilon, pi-epsilon), np.random.uniform(-0.01, 0.01, dimensions)))
        while(len(population) < 9):
            bird = Bird(np.random.uniform(0+epsilon, 1-epsilon), np.random.uniform(0+epsilon, 1-epsilon), np.random.uniform(0+epsilon, pi-epsilon), np.random.uniform(-0.01, 0.01, dimensions))
            population.append(bird)
        
        population = list(population)
        positions = list(g.position for g in population) #kreiraj listu pozicija od kreirane liste objekata
        #print(positions)
        tmp_res = score_solution(positions) #provjeri score
        #print(tmp_res[0])
        if tmp_res[0] > threshold: #ako je veci od thresholda, dodaj tu populaciju u listu populacija
            populations.append(population)
            
            global_best = top_five(global_best, tmp_res[0], tmp_res[1], positions)
            '''
            if tmp_res[0] > global_best_value: #provjeri da score slucajno nije veci od global_best, ako je postavi novi global_best za score i tu poziciju
                global_best_value = tmp_res[0]
                global_best_position = tmp_res[1]
                global_best_input = positions
            '''
    print('Kreirane populacije')
    w = 1 # težina kojom se množi trenutni velocity za svaki objekt
    c1 = 1  # c1, c2 su faktori kojima se množe cognitive i social težine
    c2 = 1
    gregarious_factor = 2.5*1e-3  #faktor kojim se množi gregarious težina 
    #epsilon = 1e-3 # za definiciju epsilon okoline

    it = 0

    evaluated = 0
    missed = 0
    #print(global_best_input[0])
    #for iteration in tqdm(range(max_iterations)):
    
    
    while(time.time()-start_time < 3600*hours):
        factor = getFactor(time.time()-start_time, 3600*hours)
        w*=factor
        c1*=factor
        c2*=factor
        cnt = 0
        for p in populations: # idi za svaku populaciju
            cntt = 0
            for bird in p: # idi za svaki objekt u populaciji
                if cntt == 0: #ako nije prva iteracija, lampu normaliziraj kao i prije, a kod ogledala normaliziraj samo kut
                    bird.normalize_lamp()
                else:
                    bird.normalize_mirror()
                
                #r1 i r2 su faktori koji unose nasumičnost u odabir težina, sljedeće linije izračunavaju težine
                r1, r2 = np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5)
                cognitive_velocity = c1 * r1 * np.subtract(bird.best_input, bird.position)
                #print(global_best_position)
                social_velocity = c2 * r2 * np.subtract(global_best_input[cntt], bird.position)
                gregarious_velocity = gregarious_factor * np.subtract(np.mean([g.position for g in p], axis=0), bird.position)
                
                #provjeri je li velocity u epsilon okolini (0,0,0), ako je generiraj ga ponovno, ako nije izračunaj ga po formuli dolje
                if norm(bird.velocity, 2) < epsilon/100:
                    bird.velocity = np.random.uniform(-0.01,0.01, dimensions) 
                    restart_velocity +=1
                else:  
                    bird.velocity = (w * bird.velocity +
                                    cognitive_velocity +
                                    social_velocity + 
                                    gregarious_velocity)
                
                bird.velocity[1] /= 10
                #bird.velocity[2] /= 10
                
                np.clip(bird.velocity, -0.1, 0.1, out=bird.velocity) #ograniči velocity na interval (-0.1, 0.1)

                '''opis funkcije checkPosition gore u klasi, ako vrati true, dodaj velocity na trenutnu poziciju objekta, inače generiraj
                novi poziciju objekta'''
                
                if cntt == 0:
                    tmp = np.add(bird.position, bird.velocity/100)
                    bird.setPosition(tmp)
                else:
                    tmp = np.add(bird.position, bird.velocity)
                    bird.setPosition(tmp)
                    t_x += bird.velocity[0]
                    t_y += bird.velocity[1]
                    t_alpha += bird.velocity[2]
                    total += 1
                
                if bird.checkPosition(epsilon):
                    pass
                elif cntt > 0:
                    restart_position += 1
                    bird.setPosition(np.random.uniform(0+epsilon, 1-epsilon, dimensions))

                
                np.clip(bird.position, 0+epsilon, 1-epsilon, out=bird.position)#ograniči poziciju objekta na interval (0,1)
                #bird.setPosition(tmp)
                
                if cntt == 0: #ako je objekt lampa, denormaliziraj kao lampu, inace denormaliziraj kao ogledalo
                    bird.denormalize_lamp() #denormaliziraj objekt
                else:
                    bird.denormalize_mirror()
                cntt+=1

            '''linija ispod stvara listu pozicija objekata koje ćemo predati funkciji score_solution, dogovorili smo se da ne 
            predajemo objekte klase nego pozicije
            '''
            positions = list(g.position for g in p) 
            #current_value = random.random()
            
            #print(positions)
            
            tmp_res = score_solution(positions)
            current_value = tmp_res[0] #izračunaj score
            evaluated += 1
            if current_value == -1:
                missed += 1
            if math.isnan(current_value):
                print('nan: ', positions)
                print(f'score {current_value}')

            '''provjeri je li score za populaciju bolji od trenutnog najboljeg, ako je postavi tu vrijednost kao najbolju za tu
            populaciju i postavi tu poziciju objekata kao novu najbolju poziciju objekata'''

            if current_value > best_values_per_population[cnt].best_value:
                best_values_per_population[cnt].best_value = current_value
                best_values_per_population[cnt].best_position = tmp_res[1]
                best_values_per_population[cnt].best_input = positions
                
                #print(best_values_per_population[0].best_position)

                for i in range(9): #potrebno za cognitive velocity
                    populations[cnt][i].best_input = (best_values_per_population[cnt].best_input[i])
                    #print()
            #print(best_values_per_population[0].best_position)
            
            cnt +=1
        
        
        #print(list(xx.best_position for xx in best_values_per_population)[:5])
        current_global_best = max(best_values_per_population, key=lambda p: p.best_value) #vraća objekt koji ima najbolju vrijednost scorea od svih populacija
        #print(current_global_best.best_value, current_global_best.best_position)
        '''provjerava je li trenutno izračunati current_global_best bolji od dosad najboljeg scorea, 
        ako je, postavi tu vrijednost kao najbolju i postavi te pozicije objekata kao najbolje'''
        global_best = top_five(global_best, current_global_best.best_value, current_global_best.best_position, current_global_best.best_input)
        '''
        if current_global_best.best_value > global_best_value:
            
            global_best_value = current_global_best.best_value
            global_best_position = current_global_best.best_position
            global_best_input = current_global_best.best_input
        '''
        
        if it%checkpoint == 0:
            print(f"Iteration {it + 1}, miss percentage: {(missed/evaluated) * 100}%, Global Best Value: {list(global_best.keys())[0]}")

            #za zapis checkpointa
            '''
            file = open("checkpoints.txt", "a")
            file.write(f"Iteration {it + 1}/{max_iterations}, Global Best Value: {list(global_best.keys())[0]}, Global Best Position: {global_best[list(global_best.keys())[0]]}\n")
            file.write("###############################################################")
            file.close()
            '''
        it+=1
        #print(global_best_position)

    #return global_best_position, global_best_value, global_best_input

def denormalize(arr):
    for i in range(len(arr)):
        arr[i] = np.array(arr[i])
        if i == 0:
            #print(arr[i][0])
            arr[i][0]*=19
            arr[i][1]*=19
            arr[i][2]*=pi
        else:
            arr[i][2]*=pi
            
    return arr
            
    
        
try:
    num_particles = 10  #broj populacija koje stvaramo
    #dimensions = 27
    max_iterations = 100000
    #best_position, best_value, best_input = gpso(num_particles, max_iterations, hours=7, threshold=-2)
    gpso(num_particles, max_iterations, hours=4, threshold=0.1)
    end_time = time.time()
    #print(best_position)
    best_values = list(global_best.keys())
    best_positions = list()
    best_inputs = list()
    for k in best_values:
        v = global_best[k]
        #print(v[0])
        #print(v[1])
        best_positions.append(v[0])
        best_inputs.append(v[1])
    
    
    print("Global best values: ", best_values)
    print("Global best positions: ", best_positions)
    print("Global best inputs: ", best_inputs)
    
    print(f"Avg t_x iznosi{t_x/total}, avg t_y iznosi {t_y/total}, avg t_alpha iznosi {t_alpha/total}")
    
    print(f"Vrijeme izvođenja je {end_time-start_time} sekundi")
except KeyboardInterrupt:
    print('stopped')
    #print(global_best)
    best_values = list(global_best.keys())
    #print(best_values)
    best_positions = list()
    best_inputs = list()
    for k in best_values:
        v = global_best[k]
        #print(v[0])
        #print(v[1])
        best_positions.append(v[0])
        best_inputs.append(v[1])
    
    
    print("Global best values: ", best_values)
    print("Global best positions: ", best_positions)
    print("Global best inputs: ", best_inputs)
    
    print(f"Avg t_x iznosi{t_x/total}, avg t_y iznosi {t_y/total}, avg t_alpha iznosi {t_alpha/total}")
