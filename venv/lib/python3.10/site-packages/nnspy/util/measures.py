from ctypes import c_double, c_int
from nnspy.device.component import connected_component
from nnspy.device.network import network_state
from nnspy.nns import nns

nns.resistive_distance.argtypes = network_state, connected_component, c_int, c_int
nns.resistive_distance.restype = c_double

__all__ = "nns",
