from ctypes import c_double, c_int, POINTER
from nnspy.device.network import network_state
from nnspy.device.component import connected_component
from nnspy.interface.interface import interface
from nnspy.interface.mea import MEA
from nnspy.nns import nns

nns.voltage_stimulation.argtypes = network_state, connected_component, interface, POINTER(c_double)
nns.voltage_stimulation.restype = c_int

nns.voltage_stimulation_mea.argtypes = network_state, connected_component, MEA, POINTER(c_double)
nns.voltage_stimulation_mea.restype = c_int

__all__ = "nns",
