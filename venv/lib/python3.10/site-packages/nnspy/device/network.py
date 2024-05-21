from ctypes import c_double, c_int, c_void_p, POINTER, Structure
from nnspy.device.datasheet import datasheet
from nnspy.device.junction import junction
from nnspy.device.wire import wire
from nnspy.nns import nns

class network_topology(Structure):
    _fields_ = [
        ("Ws",          POINTER(wire)),
        ("js_count",    c_int),
        ("Js",          POINTER(junction))
    ]

class network_state(Structure):
    _fields_ = [
        ("Ys",          POINTER(c_double)),
        ("Vs",          POINTER(c_double))
    ]

nns.create_network.argtypes = datasheet, POINTER(c_int), POINTER(c_int)
nns.create_network.restype = network_topology

nns.construe_circuit.argtypes = datasheet, network_topology
nns.construe_circuit.restype = network_state

nns.ntcmp.argtypes = c_void_p, c_void_p
nns.ntcmp.restype = c_int

nns.copy_topology.argtypes = datasheet, network_topology
nns.copy_topology.restype = network_topology

nns.copy_state.argtypes = datasheet, network_topology, network_state
nns.copy_state.restype = network_state

nns.destroy_topology.argtypes = network_topology,

nns.destroy_state.argtypes = network_state,

__all__ = "network_state", "network_topology", "nns",
