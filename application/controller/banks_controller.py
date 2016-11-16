from dao.BankDao import BankDao

from application.controller.controller import Controller
from application.controller.device_controller import DeviceController
from application.controller.notification_controller import NotificationController

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch

from pluginsmanager.model.update_type import UpdateType


class BanksController(Controller):
    """
    Manage :class:`Bank`, creating new, updating or deleting.
    """

    def __init__(self, application):
        super(BanksController, self).__init__(application)
        self.dao = None

        self.manager = None
        self.currentController = None
        self.deviceController = None
        self.notifier = None

    def configure(self):
        self.dao = self.app.dao(BankDao)

        self.manager = BanksManager()
        self.manager.append(Bank('Empty Bank'))
        self.manager.banks[0].patches.append(Patch('Empty patch'))

        # To fix Cyclic dependece
        from application.controller.current_controller import CurrentController
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notifier = self.app.controller(NotificationController)

    @property
    def banks(self):
        return self.manager.banks

    def create_bank(self, bank, token=None):
        """
        Persists a new :class:`Bank` in database.

        :param Bank bank: Bank that will be added
        :param string token: Request token identifier
        :return int: bank index
        """
        # TODO - Save
        self.manager.append(bank)

        self._notify_change(bank, UpdateType.CREATED, token)

        return self.manager.banks.index(bank)

    def update_bank(self, bank, token=None):
        """
        Notify all observers that the :class:`Bank` object has updated
        and persists the new state.

        .. note::
            If you're changing a bank that has a current patch,
            the patch should be fully charged and loaded. So, prefer the use
            of other Controllers methods for simple changes.

        :param Bank bank: Bank updated
        :param string token: Request token identifier
        """
        # TODO - Save
        # TODO - Current bank
        if self.currentController.is_current_bank(bank):
            current_patch = self.currentController.current_patch
            self.deviceController.loadPatch(current_patch)

        self._notify_change(bank, UpdateType.UPDATED, token)

    def delete_bank(self, bank, token=None):
        """
        Remove the informed :class:`Bank`.

        .. note::
            If the Bank contains deleted contains the current patch,
            another patch will be loaded and it will be the new current patch.

        :param Bank bank: Bank to be removed
        :param string token: Request token identifier
        """
        # TODO - Save
        if bank == self.currentController.current_bank:
            self.currentController.to_next_bank()

        self.manager.banks.remove(bank)

        self._notify_change(bank, UpdateType.DELETED, token)

    def swap(self, bank_a, bank_b, token=None):
        """
        Swap bank_a with bank_b
        """
        index_a = self.banks.index(bank_a)
        index_b = self.banks.index(bank_b)

        self.banks[index_a], self.banks[index_a] = self.banks[index_b], self.banks[index_a]

        # TODO - Save

        self._notify_change(bank_a, UpdateType.UPDATED, token)
        self._notify_change(bank_b, UpdateType.UPDATED, token)

    def _notify_change(self, bank, update_type, token=None):
        self.notifier.bank_updated(bank, update_type, token)
