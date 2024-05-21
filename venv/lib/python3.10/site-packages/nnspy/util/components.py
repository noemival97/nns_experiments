from ctypes import c_int, POINTER
from nnspy.device.component import connected_component
from nnspy.device.datasheet import datasheet
from nnspy.device.network import network_topology
from nnspy.nns import nns

nns.split_components.argtypes = datasheet, network_topology, POINTER(c_int), c_int
nns.split_components.restype = POINTER(connected_component)

__all__ = "nns",
