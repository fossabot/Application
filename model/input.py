from abc import ABCMeta

from unittest.mock import MagicMock


class Input(metaclass=ABCMeta):

    def __init__(self, effect):
        self._effect = effect

        self.observer = MagicMock()

    @property
    def effect(self):
        return self._effect
