from application.controller.controller import Controller
from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController
from application.controller.effect_controller import EffectController
from application.controller.notification_controller import NotificationController
from application.controller.param_controller import ParamController

from dao.CurrentDao import CurrentDao


class CurrentController(Controller):
    """
    Manage the current :class:`Bank` and current :class:`Patch`
    """

    def __init__(self, application):
        super(CurrentController, self).__init__(application)
        self.dao = None
        self.bank_number = 0
        self.patch_number = 0

        self.device_controller = None
        self.banks_controller = None
        self.effect_controller = None
        self.notifier = None
        self.param_controller = None

    def configure(self):
        self.device_controller = self.app.controller(DeviceController)
        self.banks_controller = self.app.controller(BanksController)
        self.effect_controller = self.app.controller(EffectController)
        self.notifier = self.app.controller(NotificationController)
        self.param_controller = self.app.controller(ParamController)

        self.dao = self.app.dao(CurrentDao)
        data = self.dao.load()
        self.bank_number = 0#data["bank"]
        self.patch_number = 0#data["patch"]

    # ************************
    # Property
    # ************************

    @property
    def current_patch(self):
        """
        Get the current :class:`Patch`
        """
        return self.current_bank.patches[self.patch_number]

    @property
    def current_bank(self):
        """
        Get the :class:`Bank` that contains the current :class:`Patch`
        """
        return self.banks_controller.banks[self.bank_number]

    # ************************
    # Persistance
    # ************************
    def _save_current(self):
        self.dao.save(self.bank_number, self.patch_number)

    # ************************
    # Get of Current
    # ************************
    def is_current_bank(self, bank):
        """
        :param Bank bank:
        :return bool: The :class:`Bank` is the current bank?
        """
        return bank == self.current_bank

    def is_current_patch(self, patch):
        """
        :param Patch patch:
        :return bool: The :class:`Patch` is the current patch?
        """
        return self.is_current_bank(patch.bank) and self.current_patch == patch

    # ************************
    # Set Current Patch/Bank
    # ************************
    def to_before_patch(self, token=None):
        """
        Change the current :class:`Patch` for the previous patch.

        If the current patch is the first in the current :class:`Bank`,
        the current patch is will be the **last of the current Bank**.

        :param string token: Request token identifier
        """
        before_patch_number = self.patch_number - 1
        if before_patch_number == -1:
            before_patch_number = len(self.current_bank.patches) - 1

        self.set_patch(self.current_bank.patches[before_patch_number], token)

    def to_next_patch(self, token=None):
        """
        Change the current :class:`Patch` for the next patch.

        If the current patch is the last in the current :class:`Bank`,
        the current patch is will be the **first of the current Bank**

        :param string token: Request token identifier
        """
        next_patch_number = self.patch_number + 1
        if next_patch_number == len(self.current_bank.patches):
            next_patch_number = 0

        self.set_patch(self.current_bank.patches[next_patch_number], token)

    def set_patch(self, patch, token=None):
        """
        Set the current :class:`Patch` for the patch
        only if the ``patch != current_patch``

        :param Patch patch: New current patch
        :param string token: Request token identifier
        """
        if self.is_current_patch(patch):
            return

        self._set_current(patch, token=token)

    def to_before_bank(self, token=None):
        """
        Change the current :class:`Bank` for the before bank. If the current
        bank is the first, the current bank is will be the last bank.

        The current patch will be the first of the new current bank.

        :param string token: Request token identifier
        """
        banks = self.banks_controller.banks
        position = self.bank_number

        before_index = position - 1
        if before_index == -1:
            before_index = len(banks) - 1

        self.set_bank(banks[before_index], token=token)

    def to_next_bank(self, token=None):
        """
        Change the current :class:`Bank` for the next bank. If the current
        bank is the last, the current bank is will be the first bank.

        The current patch will be the first of the new current bank.

        :param string token: Request token identifier
        """
        banks = self.banks_controller.banks
        position = self.bank_number

        next_index = position + 1
        if next_index == len(banks):
            next_index = 0

        self.set_bank(banks[next_index], token=token)

    def set_bank(self, bank, token=None, notify=True):
        """
        Set the current :class:`Bank` for the bank
        only if the ``bank != current_bank``

        :param Bank bank: Bank that will be the current
        :param string token: Request token identifier
        :param bool notify: If false, not notify change for :class:`UpdatesObserver`
                            instances registered in :class:`Application`
        """
        if self.current_bank == bank:
            return

        self._set_current(bank.patches[0], token, notify)

    def _set_current(self, patch, token=None, notify=True):
        bank_number = self.banks_controller.banks.index(patch.bank)
        patch_number = patch.bank.patches.index(patch)

        self._load_device_patch(  # throwable. need be first
            bank_number,
            patch_number
        )
        self.bank_number = bank_number
        self.patch_number = patch_number

        self._save_current()

        if notify:
            self.notifier.current_patch_changed(self.current_patch, token)

    def _load_device_patch(self, bankNumber, patchNumber):
        bank = self.banks_controller.banks[bankNumber]
        patch = bank.patches[patchNumber]

        self.device_controller.loadPatch(patch)
