from abc import ABCMeta, abstractmethod

from unittest.mock import MagicMock


class Effect(metaclass=ABCMeta):
    """
    Representation of a audio plugin instance.

    Effect contains a `active` status (off=bypass), a list of :class:`Param`,
    a list of :class:`Input` and a list of :class:`Connection`
    """

    def __init__(self):
        self._params = []
        self._inputs = []
        self._outputs = []

        self._active = True

        self.observer = MagicMock()

    @property
    @abstractmethod
    def params(self):
        """
        :return list[Param]: Params of effect
        """
        ...

    @property
    @abstractmethod
    def inputs(self):
        """
        :return list[Input]: Inputs of effect
        """
        ...

    @property
    @abstractmethod
    def outputs(self):
        """
        :return list[Output]: Outputs of effect
        """
        ...

    @property
    def active(self):
        """
        Is effect active?
        ``Active false = Inactive = bypass``

        :return bool: Effect status.
        """
        return self._active

    @active.setter
    def active(self, status):
        """
        Set effect status

        :param bool status: Effect status when ``True`` is active
                            ``False`` is inactive (bypass)
        """
        if status == self._active:
            return

        self._active = status
        self.observer.onEffectStatusToggled(self)

    def toggle(self):
        """
        Toggle the effect status: ``self.active = not self.active``
        """
        self.active = not self.active
