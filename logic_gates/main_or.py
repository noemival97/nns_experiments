import sys
import os

# Aggiungi la directory del modulo al percorso di ricerca
sys.path.append(os.path.abspath("./nns.py-master/logic_gates"))
import genetic_all
import utils

if __name__ == "__main__":
    seed = int(sys.argv[1])  
    genetic_all.genetic("OR",seed) 