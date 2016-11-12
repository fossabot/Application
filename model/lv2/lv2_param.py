from model.param import Param


class Lv2Param(Param):
    """
    :class:`Param` is an object representation of an Lv2 Audio Plugin
    Parameter

    :param value: Param value
    """

    def __init__(self, param):
        super(Lv2Param, self).__init__(param['ranges']['default'])
        self._param = param

    @property
    def maximum(self):
        return self._param['ranges']['maximum']

    @property
    def minimum(self):
        return self._param['ranges']['minimum']
