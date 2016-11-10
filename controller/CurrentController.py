# -*- coding: utf-8 -*-
from controller.Controller import Controller
from controller.BanksController import BanksController
from controller.DeviceController import DeviceController
from controller.EffectController import EffectController
from controller.NotificationController import NotificationController
from controller.ParamController import ParamController

from dao.CurrentDao import CurrentDao


class CurrentController(Controller):
    """
    Manage the current :class:`Bank` and current :class:`Patch`
    """
    dao = None
    bankNumber = 0
    patchNumber = 0

    deviceController = None
    banksController = None
    effectController = None
    notificationController = None
    paramController = None

    def configure(self):
        self.dao = self.app.dao(CurrentDao)
        data = self.dao.load()
        self.bankNumber = data["bank"]
        self.patchNumber = data["patch"]

        self.deviceController = self.app.controller(DeviceController)
        self.banksController = self.app.controller(BanksController)
        self.effectController = self.app.controller(EffectController)
        self.notificationController = self.app.controller(NotificationController)
        self.paramController = self.app.controller(ParamController)

    # ************************
    # Property
    # ************************

    @property
    def currentPatch(self):
        """
        Get the current :class:`Patch`
        """
        return self.currentBank.patches[self.patchNumber]

    @property
    def currentBank(self):
        """
        Get the :class:`Bank` that contains the current :class:`Patch`
        """
        return self.banksController.banks[self.bankNumber]

    # ************************
    # Persistance
    # ************************
    def _save_current(self):
        self.dao.save(self.bankNumber, self.patchNumber)

    # ************************
    # Effect
    # ************************
    def toggleStatusEffect(self, effect_index, token=None):
        """
        Toggle the status of an :class:`Effect` that belongs to the
        current :class:`Patch`

        :param int effect_index: Effect index
        :param string token: Request token identifier
        """
        effect = self.currentPatch.effects[effect_index]
        self.effectController.toggleStatus(effect, token)

    def setEffectParam(self, effect_index, param_index, new_value, token=None):
        """
        Set a :class:`Param` value of an :class:`Effect` that belongs to the
        current :class:`Patch`

        :param int effect_index: Effect index in the current patch
        :param int param_index: Param index in the effect
        :param new_value: New value of the parameter
        :param string token: Request token identifier
        """
        effect = self.currentPatch.effects[effect_index]
        param = effect.params[param_index]

        self.paramController.updateValue(param, new_value, token)

    # ************************
    # Get of Current
    # ************************
    def isCurrentBank(self, bank):
        """
        :param Bank bank:
        :return bool: The :class:`Bank` is the current bank?
        """
        return bank.index == self.bankNumber

    def isCurrentPatch(self, patch):
        """
        :param Patch patch:
        :return bool: The :class:`Patch` is the current patch?
        """
        return self.isCurrentBank(patch.bank) and self.currentPatch == patch

    # ************************
    # Set Current Patch/Bank
    # ************************
    def toBeforePatch(self, token=None):
        """
        Change the current :class:`Patch` for the previous patch.

        If the current patch is the first in the current :class:`Bank`,
        the current patch is will be the **last of the current Bank**.

        :param string token: Request token identifier
        """
        before_patch_number = self.patchNumber - 1
        if before_patch_number == -1:
            before_patch_number = len(self.currentBank.patches) - 1

        self.setPatch(before_patch_number, token)

    def toNextPatch(self, token=None):
        """
        Change the current :class:`Patch` for the next patch.

        If the current patch is the last in the current :class:`Bank`,
        the current patch is will be the **first of the current Bank**

        :param string token: Request token identifier
        """
        next_patch_number = self.patchNumber + 1
        if next_patch_number == len(self.currentBank.patches):
            next_patch_number = 0

        self.setPatch(next_patch_number, token)

    def setPatch(self, patch_number, token=None):
        """
        Set the current :class:`Patch` for the patch with
        ``index == patch_number`` only if the
        ``patch_number != currentPatch.index``

        :param int patch_number: Index of new current patch
        :param string token: Request token identifier
        """
        if self.patchNumber == patch_number:
            return

        self._set_current(self.bankNumber, patch_number, token=token)

    def toBeforeBank(self):
        """
        Change the current :class:`Bank` for the before bank. If the current
        bank is the first, the current bank is will be the last bank.

        The current patch will be the first of the new current bank.
        """
        banks = self.banksController.banks.all
        position = banks.index(self.currentBank)

        before = position - 1
        if before == -1:
            before = len(banks) - 1

        beforeBankIndex = banks[before].index

        self.setBank(beforeBankIndex)

    def toNextBank(self):
        """
        Change the current :class:`Bank` for the next bank. If the current
        bank is the last, the current bank is will be the first bank.

        The current patch will be the first of the new current bank.
        """
        banks = self.banksController.banks.all
        position = banks.index(self.currentBank)

        nextBankIndex = position + 1
        if nextBankIndex == len(banks):
            nextBankIndex = 0

        nextBank = banks[nextBankIndex].index

        self.setBank(nextBank)

    def setBank(self, bank_number, token=None, notify=True):
        """
        Set the current :class:`Bank` for the bank with
        ``index == bank_number`` only if the
        ``bank_number != currentBank.index``

        :param int bank_number: Index of new current bank
        :param string token: Request token identifier
        :param bool notify: If false, not notify change for :class:`UpdatesObserver`
                            instances registred in :class:`Application`
        """
        if self.bankNumber == bank_number:
            return

        self._set_current(bank_number, 0, token, notify)

    def _set_current(self, bankNumber, patchNumber, token=None, notify=True):
        self._load_device_patch(  # throwable. need be first
            bankNumber,
            patchNumber
        )
        self.bankNumber = bankNumber
        self.patchNumber = patchNumber
        self._save_current()

        if notify:
            self.notificationController.notifyCurrentPatchChange(self.currentPatch, token)

    def _load_device_patch(self, bankNumber, patchNumber):
        bank = self.banksController.banks[bankNumber]
        patch = bank.patches[patchNumber]

        self.deviceController.loadPatch(patch)
