from model.output import Output


class Lv2Output(Output):

    def __init__(self, effect, output):
        super(Lv2Output, self).__init__(effect)
        self._output = output
