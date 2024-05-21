  
  # define the Input and Control voltage values
IV = 5
PIN = list(range(0, 16))

CHECK = {
    "AND": [0, 0, 0, 1],
    "OR": [0, 1, 1, 1],
    "NOR": [1, 0, 0, 0],
    "NAND": [1, 1, 1, 0],
    "XOR": [0, 1, 1, 0],
    "NOTXOR": [1,0,0,1]
} 

def input_conf(pins,CV):
    indici = sorted(range(len(pins)), key=lambda x: pins[x])
    if indici==[2,1,0] :
        return [
        (-IV,  CV, -IV),
        (IV, CV, -IV),
        (-IV,  CV, IV),
        (IV, CV, IV)
        ], (0,CV,0)
            # define the inputs to the gate
    elif indici==[0,1,2]:
                return [
        (-IV,  CV, -IV),
        (-IV, CV, IV),
        (IV,  CV, -IV),
        (IV, CV, IV)
        ], (0,CV,0)
    elif indici==[1,0,2]:
        return [
        (CV,  -IV, -IV),
        (CV, IV, -IV),
        (CV, -IV, IV),
        (CV, IV, IV)
    ], (CV,0,0)
    elif indici==[1,2,0]:
        return [
        (CV,  -IV, -IV),
        (CV, -IV, IV),
        (CV, IV, -IV),
        (CV, IV, IV)
    ], (CV,0,0)
    elif indici==[0,2,1]:
           return [
        (-IV, -IV,CV,),
        (IV, -IV, CV),
        (-IV, IV, CV),
        (IV, IV, CV)
    ], (0,0,CV)
    elif indici==[2,0,1]:
           return [
        (-IV, -IV,CV,),
        (-IV, IV, CV),
        (IV, -IV, CV),
        (IV, IV, CV)
    ], (0,0,CV)

def check_v(v):
    return max(-IV, min(v,IV))

