  
import numpy as np 
import random
 # define the Input and Control voltage values

PIN = list(range(0, 16))
IV= 5
CHECK = {
    "AND": [0, 0, 0, 1],
    "OR": [0, 1, 1, 1],
    "NOR": [1, 0, 0, 0],
    "NAND": [1, 1, 1, 0],
    "XOR": [0, 1, 1, 0],
    "NOTXOR": [1,0,0,1]
} 

MU_N = 0.0
SIG_N = 0.5

def input_conf(pins,cv, noise):
    indici = sorted(range(len(pins)), key=lambda x: pins[x])
    if noise:
        noise=np.random.normal(MU_N,SIG_N,3)
        iv1= IV + noise[0]
        iv2=IV+ noise[1]
        cv+=noise[2]
        print(iv1,)
        print(f'Rumore in ingresso1 :{noise[0]}' )
        print(f'Rumore in ingresso2 : { noise[1]}')
        print(f'Rumore di controllo  : { noise[2]}')
    else: 
        iv1=IV
        iv2=IV


    if indici==[2,1,0] :
        return [
        (-iv2,  cv, -iv1),
        (iv2, cv, -iv1),
        (-iv2,  cv, iv1),
        (iv2, cv, iv1)
        ], (0,cv,0)
            # define the inputs to the gate
    elif indici==[0,1,2]:
                return [
        (-iv1,  cv, -iv2),
        (-iv1, cv, iv2),
        (iv1,  cv, -iv2),
        (iv1, cv, iv2)
        ], (0,cv,0)
    elif indici==[1,0,2]:
        return [
        (cv,  -iv1, -iv2),
        (cv, iv1, -iv2),
        (cv, -iv1, iv2),
        (cv, iv1, iv2)
    ], (cv,0,0)
    elif indici==[1,2,0]:
        return [
        (cv,  -iv2, -iv1),
        (cv, -iv2, iv1),
        (cv, iv2, -iv1),
        (cv, iv2, iv1)
    ], (cv,0,0)
    elif indici==[0,2,1]:
           return [
        (-iv1, -iv2,cv,),
        (iv1, -iv2, cv),
        (-iv1, iv2, cv),
        (iv1, iv2, cv)
    ], (0,0,cv)
    elif indici==[2,0,1]:
           return [
        (-iv2, -iv1,cv,),
        (-iv2, iv1, cv),
        (iv2, -iv1, cv),
        (iv2, iv1, cv)
    ], (0,0,cv)

def check_v(v):
    return max(-IV, min(v,IV))

