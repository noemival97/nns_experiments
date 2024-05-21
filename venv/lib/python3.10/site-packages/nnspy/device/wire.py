from ctypes import c_double, c_int, c_void_p, Structure
from nnspy.nns import nns
from nnspy.util.point import point

class wire(Structure):
    _fields_ = [
        ("centroid",    point),
        ("start_edge",  point),
        ("end_edge",    point),
        ("length",      c_double)
    ]

nns.wcmp.argtypes = c_void_p, c_void_p
nns.wcmp.restype = c_int

__all__ = "wire", "nns"
