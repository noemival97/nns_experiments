import utils
import nw


from deap import base
from deap import creator
from deap import tools 

import time
import random


def create_individual():
    e = random.sample(range(0, 16), 5)
    v= random.uniform(-utils.IV, utils.IV)
    t= random.uniform(-utils.IV, utils.IV)
    c=random.randint(0,1)
    return e,v,t,c

def mutate(gene,i):
    # Modifica casualmente un numero nella lista
    if i == 0:
        gene[random.randint(0,4)] =random.choice(list(set(utils.PIN)-set(gene)))   # Genera un nuovo valore casuale
    elif i == 1 or i==2:
        gene= utils.check_v(gene + random.gauss(0, 0.1))
    elif i==3 :   
        gene = random.randint(0,1)

    return gene

def cod(t,c,v_out):
    if c:
        return [1 if v >= t else 0 for v in v_out[::2]]
    else:
        return [1 if v <= t else 0 for v in v_out[::2]]
# Function to evaluate an individual's fitness
def evaluate(individual,nn):
    print(individual)
    v_outputs = nn.stimulation(individual)
    outputs = cod(individual[2],individual[3],v_outputs)
    print(v_outputs)
    point = sum(o == c for o, c in zip(outputs, utils.CHECK.get(TYPE)))
    fit = point / 4 * 100  # Assuming there are always 4 elements in check
    print(fit)
    return fit,

def termination_check(best):

    if(best.fitness.values[0]==100):
        del creator.FitnessMax
        del creator.Individual
        return True
    else: return False

def genetic(type_lg, seed):
    global TYPE
    TYPE=type_lg
    start_time=time.time()
    nn=nw.Nw(seed)
    random.seed(seed)

    POPULATION=50
    K=10
    GENERATIONS=100
    MUT_PB=0.2 #prima 0.125
    print("Experiment ",TYPE)
    print(f"Generation of {POPULATION} individual, with k top {K}, in {GENERATIONS} generation with {MUT_PB} pm")
    
    # Create a Fitness class with a single objective maximizing fitness
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # Create an Individual class representing a binary string
    creator.create("Individual", list, fitness=creator.FitnessMax)
    # Create the toolbox with the necessary components
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual) #da rivedere
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) #da ricedere 
    toolbox.register("mutate",mutate)
    toolbox.register("select", tools.selBest)
    toolbox.register("evaluate", evaluate)
    toolbox.register("clone_individual", lambda x: creator.Individual(x))
    
    population = toolbox.population(n=POPULATION)

    gen=0
    while gen<GENERATIONS:
        print(f"Generazione: {gen}\n")      
        # Evaluate the individuals with an no fitness
        no_fit_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = [toolbox.evaluate(ind, nn) for ind in no_fit_ind]

        for ind, fit in zip(no_fit_ind, fitnesses):
            ind.fitness.values = fit
        k_top= tools.selBest(population,K)
        best_individual=k_top[0]
        all_fit_values = [ind.fitness.values[0] for ind in population]
        print([ind.fitness.values[0] for ind in k_top])
        print(f"Individuo migliore: {best_individual} with fitness {best_individual.fitness.values}\n")
        print(f"Valore minimo della fitness: {min(all_fit_values)}\n")
        print(f"Media della fitness: {sum(all_fit_values) / len(population)}\n")
        print(f"Valore massimo della fitness: {best_individual.fitness.values}\n")
        
        if termination_check(best_individual) or gen==GENERATIONS-1:
            end_time = time.time()
            duration = end_time - start_time
            print(f"{type_lg} experiment end in {gen} and {duration} second ")
            print(f"Best Individual {best_individual} with fitness : {best_individual.fitness.values}")
            break

        k_top=list(map(toolbox.clone, k_top))
        #MUTATION
        offspring = []
        for parent in k_top:
            #non ricalcolo la fitness del padre
            offspring.append(parent)
        # Espandi la lista di valori mutati fino alla lunghezza della popolazione
        while len(offspring) < POPULATION:
            parent=toolbox.clone_individual(random.choice(offspring))
            # Scegli casualmente un individuo tra i k mutalo e aggiungilo alla lista
            del parent.fitness.values
            for i,gene in enumerate(parent):
                if random.random() < MUT_PB:
                    gene=toolbox.mutate(gene,i)

            offspring.append(parent)


        # Replace the old population by the offspring
        population[:] = offspring   
        gen+=1

    return best_individual,duration,gen
        
