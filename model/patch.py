from util.observable_list import ObservableList
from model.update_type import UpdateType

from unittest.mock import MagicMock


class Patch(object):
    """
    Patch is a pedalboard representation: your structure contains
    :class:`Effect` and :class:`Connection`.

    :param string name: Patch name
    """
    def __init__(self, name):
        self.name = name
        self.effects = ObservableList()
        self.connections = ObservableList()

        self.effects.observer = self._effects_observer
        self.connections.observer = self._connections_observer

        self.observer = MagicMock()

    def _effects_observer(self, update_type, effect, index):
        if update_type == UpdateType.CREATED \
        or update_type == UpdateType.UPDATED:
            effect.patch = self
            effect.observer = self.observer

        self.observer.onEffectUpdated(effect, update_type)

        if update_type == UpdateType.DELETED:
            effect.patch = None
            effect.observer = MagicMock()

    def _connections_observer(self, update_type, connection, index):
        self.observer.onConnectionUpdated(connection, update_type)

    @property
    def json(self):
        """
        Get a json decodable representation of this bank

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'name': self.name,
            'effects': [effect.json for effect in self.effects],
            'connections': [connection.json for connection in self.connections]
        }

    def append(self, effect):
        """
        Add a :class:`Effect` in this patch

        This works same as::
        >>> patch.effects.append(effect)
        or::
        >>> patch.effects.insert(len(patch.effects), effect)

        :param Effect effect: Effect that will be added
        """
        self.effects.append(effect)
