import re
import matplotlib.pyplot as plt # type: ignore
import numpy as np
from ctypes import *
from nnspy import *
import sys
import os

sys.path.append(os.path.abspath("/home/nvalentini/Documenti/nns.py/logic_gates"))
import utils

def cod(t,c,v_out):
    if c:
        return [1 if v >= t else 0 for v in v_out[::2]]
    else:
        return [1 if v <= t else 0 for v in v_out[::2]]
    
def evaluate(individual,nn,lg_type):
    v_outputs = nn.stimulation(individual)
    outputs = cod(individual[2],individual[3],v_outputs)
    point = sum(o == c for o, c in zip(outputs, utils.CHECK.get(lg_type.upper())))
    fit = point / 4 * 100  # Assuming there are always 4 elements in check
    return fit,v_outputs
import nw
# Funzione per estrarre l'individuo e i valori di fitness dalla stringa
def parse_best_individual(s):
    # Trova tutti i numeri nella stringa
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    # Estrai la lista di interi
    individual = [int(num) for num in numbers[:5]]
    return [individual] 


def get_best_data(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    dati = []
    individuo_corrente = None
    for line in lines:
        line = line.strip()
        
        if line.startswith('Individuo: '):
            individuo_corrente = eval(line.replace('Individuo:', '').strip())

        
        elif line.startswith('reti'):
            rete= eval(line.replace('reti:', '').strip())
            dati.append([individuo_corrente, rete])
    
    return dati


type_lg="xor"
risultati= get_best_data(f'./best_values_{type_lg}_noise.txt')
print(risultati)
sigma=0.1
mu=0
print(f'Start {type_lg} noise experiment with sigma {sigma} and mu {mu}')

for risultato in risultati:
    
    print("Rete:", risultato[1])
    reti= risultato[1]
    print("Individuo:", risultato[0])
    individual=risultato[0]
    for rete in reti:
        nn=nw.Nw(rete, True)
        Vs=nn.stimulation(individual)
        outpus = cod(individual[2],individual[3],Vs)
        fit,out=evaluate(individual,nn,type_lg)
        print(f'FITNESS with noise: {fit}')
        print(f'OUTPUTS with noise: {out}')

        STEPS = 2
        # plot the output
        plt.plot(range(STEPS), Vs[0:STEPS], label="0, 0")
        plt.plot(range(STEPS, STEPS * 2), Vs[STEPS:STEPS*2], label="1, 0")
        plt.plot(range(STEPS * 2, STEPS * 3), Vs[STEPS*2:STEPS*3], label="0, 1")
        plt.plot(range(STEPS * 3, STEPS * 4), Vs[STEPS*3:STEPS*4], label="1, 1")
        plt.axhline(individual[2], color="r", linestyle="--")
        plt.xlabel("Steps")
        plt.ylabel("Voltage [V]")
        plt.title(f"{type_lg.upper()} Gate")
        plt.legend()
        plt.savefig(f'./{type_lg}_result_noise/plot/sigma{utils.SIG_N.replace('.', '') }/{type_lg}{risultato[0]}.png')
