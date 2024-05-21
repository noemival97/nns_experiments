from ctypes import c_double, c_int, c_void_p, Structure
from nnspy.nns import nns

class datasheet(Structure):
    _fields_ = [
        ("wires_count",     c_int),
        ("length_mean",     c_double),
        ("length_std_dev",  c_double),
        ("package_size",    c_int),
        ("generation_seed", c_int)
    ]

nns.dscmp.argtypes = c_void_p, c_void_p
nns.dscmp.restype = c_int

__all__ = "datasheet", "nns"
