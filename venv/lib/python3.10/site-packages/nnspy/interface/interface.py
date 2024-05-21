from ctypes import c_double, c_int, c_void_p, POINTER, Structure
from nnspy.nns import nns

class interface(Structure):
    _fields_ = [
        ("sources_count",   c_int),
        ("sources_index",   POINTER(c_int)),
        ("grounds_count",   c_int),
        ("grounds_index",   POINTER(c_int)),
        ("loads_count",     c_int),
        ("loads_index",     POINTER(c_int)),
        ("loads_weight",    POINTER(c_double)),
    ]

nns.itcmp.argtypes = c_void_p, c_void_p
nns.itcmp.restype = c_int

nns.copy_interface.argtypes = interface,
nns.copy_interface.restype = interface

nns.destroy_interface.argtypes = interface,

__all__ = "interface", "nns"
