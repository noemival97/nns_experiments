from ctypes import *
from nnspy import *
import sys
import os


seed = int(sys.argv[1])

ds = datasheet()
ds.wires_count      = 2000
ds.length_mean      = 40.0
ds.length_std_dev   = 14.0
ds.package_size     = 500
ds.generation_seed  = seed

ccs_count, n2c = c_int(0), (c_int *  ds.wires_count)()
nt = nns.create_network(ds, n2c, byref(ccs_count))


print("Serializing the Nanowire Network\n")
nns.serialize_network(ds, nt, c_char_p(".".encode()), seed)

print("Deserializing the Nanowire Network\n")
loaded_ds=datasheet()
loaded_nt=network_topology()
nns.deserialize_network(byref(loaded_ds), byref(loaded_nt), c_char_p(".".encode()), seed)
print("Construing the Nanowire Network equivalent electrical circuit\n")

ns = nns.construe_circuit(ds, nt)

print("Serializing the network state\n")

nns.serialize_state(ds, nt, ns, c_char_p(".".encode()), seed, -1)

print("Deserializing the network state\n")
loaded_ns = network_state()
nns.deserialize_state(ds, nt, byref(loaded_ns), c_char_p(".".encode()), seed, -1)

print("Splitting the Nanowire Network in connected components\n")

ccs = nns.split_components(ds, nt, n2c, ccs_count)[:ccs_count.value]

print("Finding and selecting the largest connected component of the Nanowire Network\n")

cc = max(ccs, key=lambda x: int(x.ws_count))

print(f"Selected a CC with {cc.ws_count} nanowires")



print("Serializing the connected components\n")
for i in range(ccs_count.value):
    nns.serialize_component(ccs[i], c_char_p(".".encode()), seed, i)

print("Deserializing the connected components\n")

loaded_ccs=[connected_component() for _ in range(ccs_count.value)]

for i in range(ccs_count.value):
    nns.deserialize_component(byref(loaded_ccs[i]), c_char_p(".".encode()), seed, i)
print("Creating an interface to stimulate the nanowire network.\n");

sources = [cc.ws_skip]
grounds = [cc.ws_skip +cc.ws_count - 1]

loads = [int(grounds[0] / 2)]
weights = [0.5]

# Creazione dell'istanza della classe Interface
it = interface(1,
    (c_int*len(sources))(*sources),
    1,
    (c_int*len(grounds))(*grounds),
    1,
    (c_int*len(loads))(*loads),
    (c_double*len(weights))(*weights),
)
print("Serializing the network interface\n")

#serialize the network interface
nns.serialize_interface(it, c_char_p(".".encode()), seed, 0)

print("Deserializing the network interface\n");

#create a data-structure to deserialize the network interface
loaded_it=interface()

#deserialize the network interface
nns.deserialize_interface(byref(loaded_it), c_char_p(".".encode()), seed, 0)
'''
print("Performing the voltage stimulation and weight update of the nanowire network\n")
ios = (c_double * 1)()

for i in range(100):
    nns.update_conductance(ns, cc)

    ios[0] = i/20.0
    nns.voltage_stimulation(ns, cc, it, ios)

    nns.serialize_state(ds, nt, ns, c_char_p(".".encode()), 0, i)


print("Deserializing the last state of the network state\n")

#create a data-structure to deserialize the state of the network state
loaded_lns=network_state()

#deserialize the state of the network state
nns.deserialize_state(ds, nt, byref(loaded_lns), c_char_p(".".encode()), 0, 0)
'''
print("Freeing all the allocated memory\n")

#free the network topology and state
nns.destroy_topology(nt)
nns.destroy_topology(loaded_nt)
nns.destroy_state(ns)
nns.destroy_state(loaded_ns)

#note that it is not needed to free the first
#interface as its arrays where allocated in the stack
nns.destroy_interface(loaded_it)

#free the connected components data
for i in range(len(ccs)):
    nns.free(ccs[i].Is)
    nns.free(loaded_ccs[i].Is)
    
#free(ccs)

print("Terminating the simulation\n")

