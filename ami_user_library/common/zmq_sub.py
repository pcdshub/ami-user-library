import zmq
import numpy as np
from typing import Union, Any
from amitypes import Array1d, Array2d
from ami.flowchart.library.common import CtrlNode
import ami.graph_nodes as gn

RCVHWM = 5

class ZmqProc():
    def __init__(self, url):
        self.url = url
        self._socket = None
        self.data = None

    def __del__(self):
        if self._socket is not None:
            self._socket.close()
            self._socket = None

    def __call__(self, img):
        if self._socket is None:
            ctx = zmq.Context()
            self._socket = ctx.socket(zmq.SUB)
            self._socket.setsockopt(zmq.RCVHWM, RCVHWM)
            self._socket.connect(self.url)
            self._socket.setsockopt(zmq.SUBSCRIBE, b'')

        try:
            data = self._socket.recv_pyobj(zmq.NOBLOCK)
        except zmq.error.Again:
            data = None

        if data is not None:
            self.data = data

        if self.data is not None:
            shape = self.data.shape
            img[:shape[0], :shape[1]] = self.data

        return img


class ZmqSub(CtrlNode):

    """
    ZmqSub
    """

    nodeName = "ZmqSub"
    uiTemplate = [('URL', 'text', {"value": "tcp://"})]

    def __init__(self, name):
        super().__init__(
            name,
            terminals={
                "Img": {'io': 'in', 'ttype': Array2d, 'optional': False, 'group': None},
                "Out": {'io': 'out', 'ttype': Any}
            }
        )

    def to_operation(self, **kwargs):
        return gn.Map(name=self.name()+"_operation", **kwargs, func=ZmqProc(self.values['URL']))
