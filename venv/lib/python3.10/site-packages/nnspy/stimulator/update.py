from nnspy.device.network import network_state
from nnspy.device.component import connected_component
from nnspy.nns import nns

nns.update_conductance.argtypes = network_state, connected_component

__all__ = "nns",
