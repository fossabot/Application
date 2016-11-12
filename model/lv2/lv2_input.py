from model.input import Input


class Lv2Input(Input):

    def __init__(self, effect, input):
        super(Lv2Input, self).__init__(effect)
        self._input = input
