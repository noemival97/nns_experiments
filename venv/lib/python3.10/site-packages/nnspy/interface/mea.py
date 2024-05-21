from ctypes import c_double, c_int, Structure
from nnspy.device.datasheet import datasheet
from nnspy.device.network import network_topology
from nnspy.interface.interface import interface
from nnspy.util.point import point
from nnspy.nns import nns

class MEA(Structure):
    _fields_ = [
        ("Ps",      point * 16),
        ("e2n",     c_int * 16),
        ("ct",      c_int * 16),
        ("ws",      c_double * 16)
    ]

nns.connect_MEA.argtypes = datasheet, network_topology
nns.connect_MEA.restype = MEA

nns.mea2interface.argtypes = MEA,
nns.mea2interface.restype = interface

__all__ = "MEA", "nns"
