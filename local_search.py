import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

def fitness(state):
    arr = []
    j = 0
    for i in state :
        arr.append((j , i))
        j += 1

    count = 0.0

    arr.reverse()




    for i in range(len(state)): 
        current = arr.pop()
        for j in range(len(arr)):
            if current[0] == arr[j][0] or current[1] == arr[j][1] :
                count += 1

        points = digonal(current , len(state))
        for z in points :
            x,y = (z)

            if x > i and z in arr :
                count += 1

    n= 0     
    for i in range(len(state)):
        n += i 
        
    return n-count
            
        


def digonal(point , len):
    points = []
        
    x,y = (point)
    while y+1 < (len) and x+1 < (len) :
        points.append(((x+1) , (y+1)))
        x+=1
        y+=1

    x,y = (point)
    while y-1 > -1 and x-1 > -1 :
        points.append(((x-1) , (y-1)))
        x-=1
        y-=1

    x,y = (point)
    while y-1 > -1 and x+1 < (len):
        points.append(((x+1) , (y-1)))
        x+=1
        y-=1
    
    x,y = (point)
    while y+1 < (len) and x-1 > -1:
        points.append(((x-1) , (y+1)))
        x-=1
        y+=1

        

    return points


def is_goal(state):
    n= 0     
    for i in range(len(state)):
        n += i 
    
    non_attacking = fitness(state)

    if non_attacking == n :
        return True
    
    return False


def fitness_probs(population):
    fitnesses = []
    for i in population:
        fitnesses.append(fitness(i))

    sum = 0.0
    for i in fitnesses:
        sum +=  i 

    for i in range(len(fitnesses)):
        fitnesses[i] = fitnesses[i]/sum
    
    return fitnesses


def select_parents(population, probs):
    p1 , p2 = np.random.choice(len(population),2, p=probs)
    return population[p1] , population[p2]


def reproduce(parent1, parent2 ):
    n = len(parent1)
    c = np.random.randint(0 , high = n)
   
    return parent1[:c] + parent2[c:]


def mutate(state,m_rate=0.1):
    m = np.random.uniform(low= 0.0 , high= 1.0)

    if m > m_rate:
        return state

    n = len(state)
    first_sample = np.random.randint(0, high = n)
    second_sample = np.random.randint(0 , high = n)

    state = list(state)
    state[first_sample] = second_sample
    state = tuple(state)

    return state 


def genetic_algorithm(population, m_rate=0.1, max_iters=5000):
   
    num_iters = 0 
    
    best_found = False
    best_index = -1
    while num_iters < max_iters:
       
        for i in range(len(population)) :
            if is_goal(population[i]):
                best_found = True
                best_index= i 
                break 
        if best_found :
            break

        probs = fitness_probs(population)
        new_population =[]
        for i in range(len(population)):
            p1,p2 = select_parents(population, probs)
            child = reproduce(p1, p2)
            mchild = mutate(child, m_rate)
           
            new_population.append(mchild)

        
        population = new_population
        num_iters+= 1
    
   
    if best_found : 
        
        return population[best_index] , num_iters
    else :
        max = -1 
        cur_index = -1
        for i in range(len(population)):
            current_fit =fitness(population[i])
            if current_fit > max :
                max = current_fit
                cur_index = i
               
        return population[cur_index] , num_iters 

            



def visualize_nqueens_solution(n_queens, file_name):
    
    N = len(n_queens)
    nqueens_array = np.zeros((N,N) ,dtype=int)


    for i in range(N):
        nqueens_array[n_queens[i]][i] = 1
    plt.figure(figsize=(N, N))
    sns.heatmap(nqueens_array , cmap = 'Purples' , linewidths=1.5 , linecolor = 'k' , cbar = False)
    plt.savefig(file_name , format='png')
    plt.close()


    