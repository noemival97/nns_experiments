import sys
import os

# Aggiungi la directory del modulo al percorso di ricerca
sys.path.append(os.path.abspath("./nns.py-master/logic_gates"))
import genetic_all
if __name__ == "__main__":
# Verifica che ci siano abbastanza argomenti
    if len(sys.argv) < 3:
        print("Usage: python script.py <seed> <type>")
        sys.exit(1)

    # Recupera i valori dagli argomenti della riga di comando
    seed = int(sys.argv[1])
    type_lg = str(sys.argv[2])

    genetic_all.genetic(type_lg,seed) 