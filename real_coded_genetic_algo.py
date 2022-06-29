import random

from numpy import NaN
import matplotlib.pyplot as plt


class individual:
    def __init__(self, fitness=-1, obj_function_value=NaN, xbin=[]):
        self.fitness = fitness
        self.obj_function_value = obj_function_value
        self.xbin = xbin

    def __repr__(self) -> str:
        return (
            " fitness "
            + str(self.fitness)
            + " obj_function_value= "
            + str(self.obj_function_value)
            + " xbin is "
            + str(self.xbin)
            + ">\n"
        )


def get_function_value(x1, x2):
    f = 100 * ((x2 - x1) ** 2) + (1 - x2) ** 2  
    return f

#  accepts a parent and assigns fitness and obj_funtion value to it
def evaluate(parent): 
    value = get_function_value(parent.xbin[0],parent.xbin[1])        
    parent.obj_function_value = value
    parent.fitness = value


def selection(players):
    selected_players = []
    length = len(players)
    idx = random.sample(range(0, length), length)

    # assuming len(players) is an even number
    for i in range(0, length - 1, 2):
        p_1 = idx[i]
        p_2 = idx[i + 1]
        if players[p_1].fitness < players[p_2].fitness:
            selected_players.append(p_1)
        elif players[p_1].fitness > players[p_2].fitness:
            selected_players.append(p_2)
        else:
            random_no = random.random()
            if random_no <= 0.5:
                selected_players.append(p_1)
            else:
                selected_players.append(p_2)

    idx = random.sample(range(0, length), length)
    #  tournament selection done once more to get required number of players
    for i in range(0, length - 1, 2):
        p_1 = idx[i]
        p_2 = idx[i + 1]
        if players[p_1].fitness < players[p_2].fitness:
            selected_players.append(p_1)
        elif players[p_1].fitness > players[p_2].fitness:
            selected_players.append(p_2)
        else:
            random_no = random.random()
            if random_no <= 0.5:
                selected_players.append(p_1)
            else:
                selected_players.append(p_2)

    for i in range(0, N):
        selected_players[i] = players[selected_players[i]]
    return selected_players



#  SBX-crossover operator ; the function also evaluates the offspring and then returns
def crossover(parent_1 , parent_2):
    offspring_1 = individual(-1,NaN,[])
    offspring_2 = individual(-1,NaN,[])
    random_no = random.random();
    if(random_no <= crossover_probability):
        for j in range(0,no_of_binary_var):
            val_1 = parent_1.xbin[j]
            val_2 = parent_2.xbin[j]
            if(val_1 > val_2):
                val_1,val_2 = val_2,val_1
            # now val_1 <= val_2
            random_no_2 = random.random()

            temp = 1.0/(sbx_constant+1.0)
            if(random_no_2 <= 0.5):
                beta_1 = pow((2*random_no_2),(temp))
            else:
                beta_1 = pow((1/(2-2*random_no_2)),temp)
            
            random_no_2 =random.random();
                
            if(random_no_2 <= 0.5):
                beta_2 = pow((2*random_no_2),(temp))
            else:
                beta_2 = pow((1/(2-2*random_no_2)),temp)
            
            child_1 = 0.5*((val_1+val_2)-beta_1*(val_2-val_1))
            child_2 = 0.5*((val_1+val_2)+beta_2*(val_2-val_1))

            child_1 = max(lower_bound[j],child_1)
            child_1 = min(upper_bound[j],child_1)

            child_2 = max(lower_bound[j],child_2)
            child_2 = min(upper_bound[j],child_2)

            offspring_1.xbin.append(child_1)
            offspring_2.xbin.append(child_2)
    else:
        offspring_1.xbin = parent_1.xbin
        offspring_2.xbin = parent_2.xbin

    evaluate(offspring_1)
    evaluate(offspring_2)

    return offspring_1,offspring_2

            
def variation(players):
    selected_players = []
    offspring = []
    length = len(players)
    idx = random.sample(range(0, length), length)
    for i in range(0, length - 1, 2):
        player_1 = players[i]
        player_2 = players[i + 1]
        offspring1 = individual( -1, NaN, [])
        offspring2 = individual( -1, NaN, [])
        offspring1, offspring2 = crossover(player_1, player_2)
        selected_players.append(offspring1)
        selected_players.append(offspring2)

    return selected_players


def mutation(parent):
    random_no = random.random();
    if(random_no <= mutation_probability):
        for j in range(0,no_of_binary_var):
            delta = 0;
            random_no1 = random.random();
            val1 = 1/(mutation_constant+1)
            if(random_no1 <= 0.5):
                delta = pow((2*random_no1),val1) - 1
            else:
                delta = 1 - pow(2-2*random_no1 , val1)
            parent.xbin[j] = parent.xbin[j] + (upper_bound[j]-lower_bound[j])*delta
            parent.xbin[j] = max(lower_bound[j],parent.xbin[j])
            parent.xbin[j] = min(upper_bound[j],parent.xbin[j]) 

    evaluate(parent)
    return parent




N = 6
T = 1000
n = 2
pc = 1
pm = 0.6
sbx_constant = int(2)
mutation_constant = 2
population_size = N
no_of_generations = T
no_of_binary_var = n

#  for now assigning manualy
lower_bound = [-5, -5]
upper_bound = [5, 5]
#  -5<=x1<=5 && -5<=x2<=5

crossover_probability = pc
mutation_probability = pm

population = []

for i in range(0,N):
    individual_i = individual(-1,NaN,[])
    for j in range(0,n):
        random_no = random.uniform(lower_bound[j],upper_bound[j])
        individual_i.xbin.append(random_no)
    evaluate(individual_i)
    population.append(individual_i)
   

cnt = 0
current_best = population[0].fitness
overall_best = current_best
solution = []
while(cnt<=T):
    M_t = selection(population)
    Q_t = variation(M_t)

    C_t = M_t + Q_t
    sorted(C_t, key=lambda x: x.fitness)

    current_best = C_t[0].fitness
    overall_best = min(overall_best,current_best)
    solution.append(overall_best)
    print("t is " , cnt , " current best is " , current_best , "overall best is " , overall_best)
    #  F_t contains the next generation offspring of size N
    F_t = []
    for i in range(0, N):
        F_t.append(C_t[i])
    
    for i in range(0,N):
        F_t[i] = mutation(F_t[i])

    cnt = cnt+1;
    
plt.plot(solution)
plt.show()


