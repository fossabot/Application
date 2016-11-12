from abc import ABCMeta, abstractmethod

from unittest.mock import MagicMock


class ParamError(Exception):

    def __init__(self, message):
        super(ParamError, self).__init__(message)
        self.message = message


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

        if not(self.minimum <= new_value <= self.maximum):
            msg = 'New value out of range: {} [{} - {}]'.format(
                new_value,
                self.minimum,
                self.maximum
            )
            raise ParamError(msg)

        self._value = new_value
        self.observer.onParamValueChange(self)

    @property
    @abstractmethod
    def minimum(self):
        ...

    @property
    @abstractmethod
    def maximum(self):
        ...

    def __repr__(self, *args, **kargs):
        return "<{} object as value={} [{} - {}] at 0x{:x}>".format(
            self.__class__.__name__,
            self.value,
            self.minimum,
            self.maximum,
            id(self)
        )
