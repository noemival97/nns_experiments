from ctypes import *
from nnspy import *

import utils


class Nw():
    def __init__(self, seed) -> None:
        
        # describe the network
        ds = datasheet()
        ds.wires_count      = 2000
        ds.length_mean      = 40.0
        ds.length_std_dev   = 14.0
        ds.package_size     = 500
        ds.generation_seed  = seed
        print("Seme della rete: ", seed)

        # create the network data

        cc_count, n2c = c_int(0), (c_int *  ds.wires_count)()
        self.nt = nns.create_network(ds, n2c, byref(cc_count))
        self.ns = nns.construe_circuit(ds, self.nt)
        self.ccs = nns.split_components(ds, self.nt,n2c, cc_count)[:cc_count.value]
        # select the largest connected component
        self.cc = max(self.ccs, key=lambda x: int(x.ws_count))
        print(f"Selected a CC with {self.cc.ws_count} nanowires")
        # connect a mea to the nanowire network
        self.mea = nns.connect_MEA(ds, self.nt)

        print("Pin connnection to CCs:")
        for i in range(4):
            for j in range(4):
                # if the electrode is disconnected, print an X
                if self.mea.e2n[i * 4 + j] == -1:
                    print("X", end="  ")
                    continue
                # print the number of the CC the electrode is connected to
                print(n2c[self.mea.e2n[i * 4 + j]], end="  ")
            print()
        print("! CHECK THAT ALL THE I/O/C ARE CONNECTED TO THE SAME COMPONENT !")

    def stimulation(self,individual):
        pins=individual[0]
        v=individual[1]
        # select the electrode to use as an output
        OUTPUT = pins[4]
        CTRL=pins[1]
        # select the electrode to use as I/O/C
        self.mea.ct[pins[0]] = 1    # SOURCE: i1
        self.mea.ct[CTRL] = 1    # SOURCE: ctrl
        self.mea.ct[pins[2]] = 1   # SOURCE: i2
        self.mea.ct[pins[3]] = 2   # GROUND  

        # convert the mea to an interface
        it = nns.mea2interface(self.mea) 


        # for each input configuration collect the output voltage
        Vs = []
        config, cv = utils.input_conf(pins[:3], v)  
        for c in config:    

            # relaxation time: avoid influence of previous evaluations
            for _ in range(200):
                ios = (c_double * 3)(0, 0, 0)   

                nns.update_conductance(self.ns, self.cc)
                nns.voltage_stimulation(self.ns, self.cc, it, ios)    

            # stimulate the network with the inputs
            for _ in range(200):
                ios = (c_double * 3)(*c)    

                nns.update_conductance(self.ns, self.cc)
                nns.voltage_stimulation(self.ns, self.cc, it, ios)    

            # read the network outputs (only the control is > 0)
            for _ in range(2):
                ios = (c_double * 3)(*cv)   

                nns.update_conductance(self.ns, self.cc)
                nns.voltage_stimulation(self.ns, self.cc, it, ios)
                Vs.append(self.ns.Vs[self.mea.e2n[OUTPUT]])


        self.mea.ct[pins[0]] = 0    # SOURCE: i1
        self.mea.ct[CTRL] = 0   # SOURCE: ctrl
        self.mea.ct[pins[2]] = 0  # SOURCE: i2
        self.mea.ct[pins[3]] = 0   # GROUND
        return Vs   

    def freeallocating(self):
        nns.destroy_topology(self.nt)
        nns.destroy_state(self.ns)
        for i in range(len(self.ccs)):

            nns.free(self.ccs[i].Is)
        nns.free(self.ccs)