from ctypes import c_char_p, c_int, POINTER
from nnspy.device.component import connected_component
from nnspy.device.datasheet import datasheet
from nnspy.device.network import network_topology, network_state
from nnspy.interface.interface import interface
from nnspy.interface.mea import MEA
from nnspy.nns import nns

nns.deserialize_network.argtypes = POINTER(datasheet), POINTER(network_topology), c_char_p

nns.deserialize_state.argtypes = datasheet, network_topology, POINTER(network_state), c_char_p, c_int, c_int

nns.deserialize_component.argtypes = POINTER(connected_component), c_char_p, c_int, c_int

nns.deserialize_interface.argtypes = POINTER(interface), c_char_p, c_int, c_int

nns.deserialize_mea.argtypes = POINTER(MEA), c_char_p, c_int, c_int

__all__ = "nns",
