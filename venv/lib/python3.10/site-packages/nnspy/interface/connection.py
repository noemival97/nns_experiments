from ctypes import c_int

NONE = c_int(0)
SOURCE = c_int(1)
GROUND = c_int(2)
LOAD = c_int(3)

__all__ = "NONE", "SOURCE", "GROUND", "LOAD"
