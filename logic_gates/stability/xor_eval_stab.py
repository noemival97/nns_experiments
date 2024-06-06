import matplotlib.pyplot as plt # type: ignore
from ctypes import *
from nnspy import *
import sys
import os
import re
sys.path.append(os.path.abspath("/home/nvalentini/Documenti/nns.py/logic_gates"))

import nw 

import utils
def cod(t,c,v_out):
    if c:
        return [1 if v >= t else 0 for v in v_out[::2]]
    else:
        return [1 if v <= t else 0 for v in v_out[::2]]

def evaluate(individual,nn):
    v_outputs = nn.stimulation(individual)
    outputs = cod(individual[2],individual[3],v_outputs)
    point = sum(o == c for o, c in zip(outputs, utils.CHECK.get("XOR")))
    fit = point / 4 * 100  # Assuming there are always 4 elements in check
    return fit,v_outputs
print("Experiment with xor restuls taken from 180 steps for stabilization")
# Funzione per estrarre l'individuo e i valori di fitness dalla stringa
def parse_best_individual(s):
    # Trova tutti i numeri nella stringa
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    # Estrai la lista di interi
    individual = [int(num) for num in numbers[:5]]
    # Estrai i valori float
    rest = [float(num) for num in numbers[5:]]
    return [individual] + rest[:-1], rest[-1]

# Lista per memorizzare i risultati delle reti

individuals = []

# Apri il file di testo in modalità di lettura
with open("./best_values_xor.txt", "r") as file:
    # Inizializza una variabile per memorizzare temporaneamente i risultati della singola rete
    risultato_rete = {}
    for riga in file:
        riga = riga.strip()  # Rimuovi eventuali spazi bianchi iniziali o finali
        if riga.startswith("rete"):
            # Se la riga inizia con "rete", abbiamo iniziato a leggere un nuovo risultato di rete
            if risultato_rete:  # Se risultato_rete non è vuoto, aggiungilo alla lista
                individuals.append(risultato_rete)
                risultato_rete = {}  # Reimposta risultato_rete per il prossimo risultato
            risultato_rete["rete"] = int(riga.split()[-1])
        elif riga.startswith("AND"):
       
            # Utilizziamo una regex per trovare il numero e i secondi
            match = re.search(r"(\d+) and (\d+\.\d+) second", riga)
            # Se la regex trova una corrispondenza, estraiamo il numero e i secondi
            if match:
                numero = int(match.group(1))
                secondi = float(match.group(2))
                risultato_rete["generazioni"]= numero
                risultato_rete["secondi"]= secondi
        elif riga.startswith("Best Individual"):
            individual, fitness_values = parse_best_individual(riga)
            risultato_rete["best_individual"]=individual
            risultato_rete["fitness"]=fitness_values
        elif riga == "no soluzione":
            # Se la riga è "no soluzione", non c'è soluzione per questa rete
            risultato_rete["soluzione"] = False

# Aggiungi l'ultimo risultato alla lista
if risultato_rete:

    individuals.append(risultato_rete)

# Example of accessing data
for individual in individuals:
    print(f'Best Individual: {individual["best_individual"]} with network {individual["rete"]} and fitness {individual["fitness"]}\n')
    print("Evaluation with other networks")
    for i in range(11):
        rete=i
        net=nw.Nw(rete, False)
        fitness,Vs_out=evaluate(individual['best_individual'],net)

        if rete == individual['rete']:
            print(f"Original fitness: ", individual['fitness'])
            print(f"Actual fitness: {fitness}, with {individual['fitness']-fitness} of difference")
        else: print(f' Individual: {individual["best_individual"]} with network {rete} and fitness {fitness}\n')

        STEPS = 2
        # plot the output
        plt.figure()
        plt.plot(range(STEPS), Vs_out[0:STEPS], label="0, 0")
        plt.plot(range(STEPS, STEPS * 2), Vs_out[STEPS:STEPS*2], label="1, 0")
        plt.plot(range(STEPS * 2, STEPS * 3), Vs_out[STEPS*2:STEPS*3], label="0, 1")
        plt.plot(range(STEPS * 3, STEPS * 4), Vs_out[STEPS*3:STEPS*4], label="1, 1")
        plt.axhline(individual['best_individual'][2], color="r", linestyle="--")
        plt.xlabel("Steps")
        plt.ylabel("Voltage [V]")
        plt.title(f"XOR {i} Gate")
        plt.legend()
        plt.savefig(f'/home/nvalentini/Documenti/nns.py/logic_gates/try/xor_evaluation_stab180/xor{individual["best_individual"]}rete_{i}.png')
        plt.close()

