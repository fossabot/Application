from model.effect import Effect
from model.lv2.lv2_param import Lv2Param

class Lv2Effect(Effect):
    """
    Representation of a Lv2 audio plugin instance.

    Effect contains a `active` status (off=bypass), a list of :class:`Param`,
    a list of :class:`Input` and a list of :class:`Connection`

    :param Lv2Plugin plugin:
    """

    def __init__(self, plugin):
        super(Lv2Effect, self).__init__()

        self.plugin = plugin
        from unittest.mock import MagicMock
        Lv2Input = MagicMock()
        Lv2Output = MagicMock()

        self._params = tuple([Lv2Param(param) for param in plugin["ports"]["control"]["input"]])
        self._inputs = tuple([Lv2Input(input_) for input_ in plugin['ports']['audio']['input']])
        self._outputs = tuple([Lv2Output(output) for output in plugin['ports']['audio']['output']])

    @property
    def params(self):
        """
        :return list[Param]: Params of effect
        """
        return self._params

    @property
    def inputs(self):
        """
        :return list[Input]: Inputs of effect
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :return list[Output]: Outputs of effect
        """
        return self._outputs
