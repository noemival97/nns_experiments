from ctypes import c_char_p, c_int, POINTER
from nnspy.device.component import connected_component
from nnspy.device.datasheet import datasheet
from nnspy.device.network import network_topology, network_state
from nnspy.interface.interface import interface
from nnspy.interface.mea import MEA
from nnspy.nns import nns

nns.serialize_network.argtypes = datasheet, network_topology, c_char_p, c_int

nns.serialize_state.argtypes = datasheet, network_topology, network_state, c_char_p, c_int, c_int

nns.serialize_component.argtypes = connected_component, c_char_p, c_int, c_int

nns.serialize_interface.argtypes = interface, c_char_p, c_int

nns.serialize_mea.argtypes = MEA, c_char_p, c_int, c_int

__all__ = "nns",
