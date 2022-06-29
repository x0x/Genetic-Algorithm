from mimetypes import init
from operator import le
import random
from re import L
from tabnanny import check
from numpy import NAN, NaN, var
from pyparsing import opAssoc
import matplotlib.pyplot as plt



class individual:
    def __init__(self, chromosome, fitness=-1, obj_function_value=NaN, xbin=[]):
        self.chromosome = chromosome
        self.fitness = fitness
        self.obj_function_value = obj_function_value
        self.xbin = xbin

    def __repr__(self) -> str:
        return (
            "< chromosome "
            + str(self.chromosome)
            + " fitness "
            + str(self.fitness)
            + " obj_function_value= "
            + str(self.obj_function_value)
            + " xbin is "
            + str(self.xbin)
            + ">\n"
        )


# x[i] = lower_limit + (upper_limit-lower_limit)/(1<<l - 1) * (DV)
def decode(string, length, l, u):

    x1 = int(0)
    for i in range(0, length):
        x1 += int(string[i]) * (1 << (length - i - 1))

    val = 1 << (int(length))

    scaling_factor = (int(u) - int(l)) / (val - 1)
    x = scaling_factor * x1

    x += l
    return x


def get_function_value(x1, x2):
    
    f = 100 * ((x2 - x1) ** 2) + (1 - x2) ** 2  
   
    return f


#  calculates the fitness and obj_funciton_value parameter for the passed individual
def evaluate(parent):
    var = []
    #  len is number of variables in the function (for now it is 2)
    len = n 
    for i in range(0, len):
        var.append(parent.xbin[i])
    parent.obj_function_value = get_function_value(var[0], var[1])
    parent.fitness = parent.obj_function_value


def binary_tournament_selection(players):

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


def single_point_crossover(parent1, parent2):
    random_no = random.random()
    offspring1 = individual("", -1, NaN, [])
    offspring2 = individual("", -1, NaN, [])

    if random_no <= crossover_probability:
        prev = 0
        child_chromosome1 = ""
        child_chromosome2 = ""
        for j in range(0, n):
            var_f1 = ""
            var_f2 = ""
            var_i1 = parent1.chromosome[prev : prev + binary_string_len[j]]
            var_i2 = parent2.chromosome[prev : prev + binary_string_len[j]]
            prev += binary_string_len[j]
            site = random.randint(0, binary_string_len[j] - 1)

            for k in range(0, site):
                var_f1 += var_i1[k]
                var_f2 += var_i2[k]
            for k in range(site, binary_string_len[j]):
                var_f1 += var_i2[k]
                var_f2 += var_i1[k]
            # print("varf1 " , var_f1)
            child_chromosome1 += var_f1
            child_chromosome2 += var_f2
            value1 = decode(
                var_f1, binary_string_len[j], lower_bound[j], upper_bound[j]
            )
            value2 = decode(
                var_f2, binary_string_len[j], lower_bound[j], upper_bound[j]
            )
            offspring1.xbin.append(value1)
            offspring2.xbin.append(value2)
        offspring1.chromosome = child_chromosome1
        offspring2.chromosome = child_chromosome2
    else:
        offspring1 = parent1
        offspring2 = parent2

    return offspring1, offspring2


def variation(players):
    selected_players = []
    offspring = []
    length = len(players)
    idx = random.sample(range(0, length), length)
    for i in range(0, length - 1, 2):
        player_1 = players[i]
        player_2 = players[i + 1]
        offspring1 = individual("", -1, NaN, [])
        offspring2 = individual("", -1, NaN, [])
        offspring1, offspring2 = single_point_crossover(player_1, player_2)
        selected_players.append(offspring1)
        selected_players.append(offspring2)

    return selected_players


def mutation(offspring):
    prev = 0
    string = ""
    for i in range(0, no_of_binary_var):
        var_i1 = offspring.chromosome[prev : prev + binary_string_len[i]]
        # print("var i1 is " , var_i1)
        var_i2 = ""
        for k in range(0, binary_string_len[i]):
            random_no_mutation = random.random()
            if random_no_mutation <= mutation_probability:
                if var_i1[k] == "1":
                    var_i2 += "0"
                else:
                    var_i2 += "1"
            else:
                var_i2 += var_i1[k]
        string += var_i2
        offspring.xbin[i] = decode(
            var_i2, binary_string_len[i], lower_bound[i], upper_bound[i]
        )
        # print("string is " ,string)
        prev += binary_string_len[i]
    offspring.chromosome = string
    evaluate(offspring)
    return



N = 64
T = 200
n = 2
pc = 1
pm = 0.6

population_size = N
no_of_generations = T
no_of_binary_var = n
#  for now assigning manualy
binary_string_len = [1000, 1000]
lower_bound = [-5, -5]
upper_bound = [5, 5]
#  -5<=x1<=5 && -5<=x2<=5

crossover_probability = pc
mutation_probability = pm

population = []

for i in range(0, N):
    individual_i = individual("", -1, -1, [])
    chromosome = ""
    for j in range(0, n):
        binary_j = ""
        for k in range(0, binary_string_len[j]):
            random_no = random.random()
            if random_no <= 0.5:
                binary_j += "0"
            else:
                binary_j += "1"
        chromosome += binary_j
        x_j = decode(binary_j, binary_string_len[j], lower_bound[j], upper_bound[j])
        individual_i.xbin.append(x_j)

    individual_i.chromosome = chromosome
    population.append(individual_i)

# print(population[0])

for i in range(0, N):
    function_value = get_function_value(population[i].xbin[0], population[i].xbin[1])
    population[i].obj_function_value = function_value
    population[i].fitness = function_value

print("initial population is ", population)
cnt = 1
overall_min = population[0].fitness
solution = []
check = []
solution.append(overall_min)
while cnt <= T:
    #  M_t is mating pool
    M_t = binary_tournament_selection(population)

    Q_t = variation(M_t)
    for i in range(0, N):
        evaluate(Q_t[i])
    #  C_t is parent union offspring . it is implemented through (mu + lambda) strategy
    C_t = M_t + Q_t
    sorted(C_t, key=lambda x: x.fitness)
    #  F_t is the survivor in this generation

    F_t = []
    for i in range(0, N):
        F_t.append(C_t[i])

    print("cnt is " , cnt , "current min fitness value is " , F_t[0].fitness , "overall min " , overall_min)
    overall_min = min(overall_min, F_t[0].fitness)
    check.append(F_t[0].fitness)
    solution.append(overall_min)
    for i in range(0, N):
            mutation(F_t[i])
    population = F_t
    cnt = cnt+1

plt.plot(solution)
plt.show()
