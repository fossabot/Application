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
from application.controller.device_controller import DeviceController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.update_type import UpdateType


class BankError(Exception):
    pass


class BanksController(Controller):
    """
    Notify all observers that a :class:`.Bank` has been created, updated, removed.
    Also makes changes to the current pedalboard when the current pedalboard bank is affected.
    """

    def __init__(self, application):
        super(BanksController, self).__init__(application)

        self.manager = self.app.autosaver.load(DeviceController.sys_effect)
        self._current = None
        self._notifier = None

    def configure(self):
        # To fix Cyclic dependence
        from application.controller.current_controller import CurrentController

        self._current = self.app.controller(CurrentController)
        self._notifier = self.app.controller(NotificationController)

    @property
    def banks(self):
        return self.manager.banks

    def created(self, bank, token=None):
        """
        Notify all observers that a new :class:`.Bank` has been created.

        .. note::

            The bank needs be added in a :class:`.BanksManager` before.

            >>> banks_manager.append(bank)
            >>> banks_controller.created(bank)

        :param Bank bank: Bank created and added in banks manager
        :param string token: Request token identifier
        """
        if bank not in self.manager.banks:
            raise BankError('Bank {} has not added in banks manager'.format(bank))

        self._notify_change(bank, UpdateType.CREATED, token, index=len(self.banks) - 1)

    def updated(self, bank, token=None, current_bank=False):
        """
        Notify all observers that the :class:`.Bank` object has updated.

        .. note::

            If a swap is realized, call this method for all the involved banks::

                >>> bank[1], bank[3] = bank[3], bank[1]
                >>> banks_controller.updated(bank[1], TOKEN)
                >>> banks_controller.updated(bank[3], TOKEN)

        .. note::

            If you're changing a bank that has a current pedalboard,
            the pedalboard should be fully charged and loaded. So, prefer the use
            of other Controllers methods for informs simple changes.

        :param Bank bank: Updated bank
        :param string token: Request token identifier
        """
        if bank not in self.manager.banks:
            raise BankError('Bank {} has not added in banks manager'.format(bank))

        if bank == self._current.bank:
            self._current.reload_current_pedalboard()

        elif current_bank:
            pedalboard_index = self._current.pedalboard.index
            self._current.set_pedalboard(bank.pedalboards[pedalboard_index])

        self._notify_change(bank, UpdateType.UPDATED, token)

    def deleted(self, bank, old_index, token=None):
        """
        Notify all observers that the :class:`.Bank` object has deleted.

        .. note::

            If the Bank deleted contains the current pedalboard,
            another pedalboard will be loaded and it will be the new current pedalboard.

        .. note::

            The bank needs be removed of the :class:`.BanksManager` before.

            >>> index = bank.index
            >>> banks_manager.banks.remove(bank)
            >>> banks_controller.deleted(bank, index)

        :param Bank bank: Removed bank
        :param int old_index: Bank index before it is removed
        :param string token: Request token identifier
        """
        if bank in self.banks:
            raise BankError('Bank {} wasn\'t deleted for banks manager'.format(bank))

        self._notify_change(bank, UpdateType.DELETED, token, index=old_index)

        if bank == self._current.bank:
            new_bank = self.banks[self._current.next_bank_index(old_index - 1)]
            self._current.set_bank(new_bank)

    def _notify_change(self, bank, update_type, token=None, index=None):
        index = index if index is not None else bank.index

        self._notifier.bank_updated(bank, update_type, index=index, origin=self.manager, token=token)
