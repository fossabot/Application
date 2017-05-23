# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from application.controller.controller import Controller
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.update_type import UpdateType


class EffectError(Exception):
    pass


class PedalboardConnectionError(Exception):
    pass


class EffectController(Controller):
    """
    Notify all observers that a :class:`.Effect` has been created, removed.
    """

    def __init__(self, application):
        super(EffectController, self).__init__(application)
        self.notifier = None

    def configure(self):
        self.notifier = self.app.controller(NotificationController)

    def created(self, effect, token=None):
        """
        Notify all observers that a new :class:`.Effect` object has been created.

        .. note::

            The effect needs be added in a :class:`.Pedalboard` before.

            >>> pedalboard.add(effect)
            >>> effect_controller.created(effect)

        :param Effect effect: Effect created and added in your pedalboard
        :param string token: Request token identifier
        """
        if effect.pedalboard is None:
            raise EffectError('Effect {} has not added in any pedalboard'.format(effect))

        self._notify_change(effect, UpdateType.CREATED, token)

    def deleted(self, effect, old_index, old_pedalboard, token=None):
        """
        Notify all observers that the :class:`.Effect` object has deleted.

        .. note::

            The effect needs be removed of your :class:`.Pedalboard` before.

            >>> pedalboard = effect.pedalboard
            >>> index = effect.index
            >>> pedalboard.effects.remove(effect)
            >>> effect_controller.deleted(effect, index, pedalboard)

        :param Effect effect: Removed effect
        :param old_index: Effect index before it is removed
        :param old_pedalboard: Pedalboard where the effect belonged
        :param string token: Request token identifier
        """
        if effect.pedalboard is not None:
            raise EffectError('Effect {} wasn\'t deleted for your pedalboard'.format(effect))

        self._notify_change(effect, UpdateType.DELETED, token, index=old_index, origin=old_pedalboard)

    def toggled_status(self, effect, token=None):
        """
        Notify all observers that the :class:`.Effect` has your status
        toggled

        :param Effect effect: Effect that your status has toggled
        :param string token: Request token identifier
        """
        if effect.pedalboard is None:
            raise EffectError('Effect {} has not added in any pedalboard'.format(effect))

        self.notifier.effect_status_toggled(effect, token)

    def _notify_change(self, effect, update_type, token, **kwargs):
        index = kwargs.pop('index') if 'index' in kwargs else effect.index
        origin = kwargs.pop('origin') if 'origin' in kwargs else effect.pedalboard

        self.notifier.effect_updated(effect, update_type, index=index, origin=origin, token=token, **kwargs)

    def connected(self, pedalboard, connection, token=None):
        """
        Notify all observers that the :class:`.Connection` object has ben created

        :param Pedalboard pedalboard: Pedalboard where has added the connection
        :param Connection connection: Connection created
        :param string token: Request token identifier
        """
        if connection not in pedalboard.connections:
            raise PedalboardConnectionError('Connection {} hasn\'t added in pedalboard'.format(connection))

        self.notifier.connection_updated(connection, UpdateType.CREATED, pedalboard=pedalboard, token=token)

    def disconnected(self, pedalboard, connection, token=None):
        """
        Notify all observers that the :class:`.Connection` object has ben removed

        :param Pedalboard pedalboard: Pedalboard where has removed the connection
        :param Connection connection: Connection removed
        :param string token: Request token identifier
        """
        if connection in pedalboard.connections:
            raise PedalboardConnectionError('Connection {} is still present on the pedalboard'.format(connection))

        self.notifier.connection_updated(connection, UpdateType.DELETED, pedalboard=pedalboard, token=token)
