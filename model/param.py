from abc import ABCMeta, abstractmethod

from unittest.mock import MagicMock


class Param(metaclass=ABCMeta):
    """
    :class:`Param` is an object representation of an Audio Plugin
    Parameter

    :param value: Param value
    """

    def __init__(self, value):
        self._value = value

        self.observer = MagicMock()

    @property
    def value(self):
        """
        :return: Param value
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        Set the param value

        :param value: New param value
        """
        if self._value == new_value:
            pass

        self.value = new_value
        self.observer.onParamValueChange(self)

    @property
    @abstractmethod
    def minimum(self):
        ...

    @property
    @abstractmethod
    def maximum(self):
        ...
