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
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.update_type import UpdateType


class PedalboardError(Exception):
    pass


class PedalboardController(Controller):
    """
    Notify all observers that a :class:`.Pedalboard` has been created, updated, removed.
    Also makes changes to the current pedalboard when the changes affects the current pedalboard.
    """

    def __init__(self, application):
        super(PedalboardController, self).__init__(application)
        self.current = None
        self.notifier = None

    def configure(self):
        self.current = self.app.controller(CurrentController)
        self.notifier = self.app.controller(NotificationController)

    def created(self, pedalboard, token=None):
        """
        Notify all observers that a new :class:`.Pedalboard` object has been created.

        .. note::

            The pedalboard needs be added in a :class:`.Bank` before.

            >>> bank.append(pedalboard)
            >>> pedalboard_controller.created(pedalboard)

        :param Pedalboard pedalboard: Pedalboard created and added in your bank
        :param string token: Request token identifier
        """
        if pedalboard.bank is None:
            raise PedalboardError('Pedalboard {} has not added in any bank'.format(pedalboard))

        self._notify_change(pedalboard, UpdateType.CREATED, token)

    def updated(self, pedalboard, token=None, reload=True):
        """
        Notify all observers that the :class:`.Pedalboard` object has updated.

        .. note::

            If a swap is realized, call this method for all the involved pedalboards::

                >>> pedalboard[1], pedalboard[3] = pedalboard[3], pedalboard[1]
                >>> pedalboard_controller.updated(pedalboard[1], TOKEN)
                >>> pedalboard_controller.updated(pedalboard[3], TOKEN)

        .. note::
            If you're changing the current pedalboard, the pedalboard should be
            fully charged and loaded if reload=True.
            So, prefer the use of other Controllers methods for simple changes.

        :param Pedalboard pedalboard: Updated pedalboard
        :param string token: Request token identifier
        :param bool reload: If it's the current pedalboard, is necessary reload the plugins?
        """
        if pedalboard.bank is None:
            raise PedalboardError('Pedalboard {} has not added in any bank'.format(pedalboard))

        if self.current.pedalboard == pedalboard and reload:
            self.current.reload_current_pedalboard()

        self._notify_change(pedalboard, UpdateType.UPDATED, token)

    def deleted(self, pedalboard, old_index, old_bank, token=None):
        """
        Notify all observers that the :class:`.Pedalboard` object has deleted.

        .. note::
            If the pedalboard is the current, another pedalboard will be loaded
            and it will be the new current pedalboard.

        .. note::

            The pedalboard needs be removed of your :class:`.Bank` before.

            >>> bank = pedalboard.bank
            >>> index = pedalboard.index
            >>> bank.pedalboards.remove(pedalboard)
            >>> pedalboard_controller.deleted(pedalboard, index, bank)

        :param Pedalboard pedalboard: Removed pedalboard
        :param old_index: Pedalboard index before it is removed
        :param old_bank: Bank where the pedalboard belonged
        :param string token: Request token identifier
        """
        if pedalboard.bank is not None:
            raise PedalboardError('Pedalboard {} wasn\'t deleted for your bank'.format(pedalboard))

        if self.current.pedalboard == pedalboard:
            self.current.to_next_pedalboard()  # ERROR

        self._notify_change(pedalboard, UpdateType.DELETED, token, index=old_index, origin=old_bank)

    def moved(self, pedalboard, old_index, token=None):
        """
        Notify all observers that the :class:`.Pedalboard` object has moved from a new position
        (pedalboard has DELETED in ``index=old_position``
        and has CREADED in the ``index=pedalboard.index``).

        .. note::

            It's necessary after moves the pedalboard position with ``move()`` method::

            >>> old_index = 3
            >>> new_index = 1
            >>> pedalboard = pedalboards[old_index]
            >>> pedalboards.move(pedalboard, new_index)
            >>> self.controller.moved(pedalboard, old_index, TOKEN)

        :param Pedalboard pedalboard: Pedalboard that will be the position in your bank changed
        :param int old_index: Original (old) index position of the pedalboard
        :param string token: Request token identifier
        """
        current_pedalboard = self.current.current_pedalboard

        self._notify_change(pedalboard, UpdateType.DELETED, token=token, index=old_index)
        self._notify_change(pedalboard, UpdateType.CREATED, token=token)

        # Save the current pedalboard data
        # The current pedalboard index changes then changes the pedalboard order
        if current_pedalboard.bank == pedalboard.bank:
            self.current._set_current(current_pedalboard, notify=False)

    def _notify_change(self, pedalboard, update_type, token=None, **kwargs):
        index = kwargs.pop('index', pedalboard.index)
        origin = kwargs.pop('origin', pedalboard.bank)

        self.notifier.pedalboard_updated(pedalboard, update_type, index=index, origin=origin, token=token, **kwargs)
