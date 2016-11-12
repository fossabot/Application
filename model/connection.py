

class ConnectionError(Exception):
    def __init__(self, message):
        super(ConnectionError, self).__init__(message)
        self.message = message


class Connection(object):
    """
    :class:`Connection` represents a connection between two
    distinct effects

    :param Output effect_output:
    :param Input effect_input:
    """

    def __init__(self, effect_output, effect_input):
        if effect_output.effect == effect_input.effect:
            ConnectionError('Effect of output and effect of input are equals')

        self._output = effect_output
        self._input = effect_input

    @property
    def output(self):
        return self._output

    @property
    def input(self):
        return self._input
