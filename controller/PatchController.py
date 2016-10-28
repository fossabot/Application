# -*- coding: utf-8 -*-
from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController

from model.Patch import Patch
from model.UpdatesObserver import UpdateType


class PatchController(Controller):
    """
    Manage :class:`Patch`, creating new, updating or deleting.
    """
    dao = None
    currentController = None
    deviceController = None
    notificationController = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def createPatch(self, bank, patch_data, token=None):
        """
        Persists a new :class:`Patch` in the :class:`Bank` informed.

        :param Bank bank: Bank that will be added to the patch
        :param dict patch_data: Patch data information
        :param string token: Request token identifier
        :return int: Index of Patch created
        """
        patch = Patch(patch_data)
        bank.addPatch(patch)
        self.dao.save(bank)

        self._notify_change(patch, UpdateType.CREATED, token)

        return len(bank.patches) - 1

    def updatePatch(self, patch, data, token=None):
        """
        Updates a :class:`Patch` object based in data parsed.

        .. note::
            If you're changing the current patch, the patch should be
            fully charged and loaded. So, prefer the use of other Controllers
            methods for simple changes.

        :param Patch patch: Patch to be updated
        :param dict data: New patch data
        :param string token: Request token identifier
        """
        patch.json = data

        self.dao.save(patch.bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.loadPatch(patch)

        self._notify_change(patch, UpdateType.UPDATED, token)

    def deletePatch(self, patch, token=None):
        """
        Remove the informed :class:`Patch`.

        .. note::
            If the patch is the current, another patch will be loaded
            and it will be the new current patch.

        :param Patch patch: Patch to be removed
        :param string token: Request token identifier
        """
        bank = patch.bank

        if self.currentController.isCurrentPatch(patch):
            self.currentController.toNextPatch()

        self._notify_change(patch, UpdateType.DELETED, token)
        del bank['patches'][patch.index]

        self.dao.save(bank)

    def swapEffects(self, effectA, effectB):
        """
        .. deprecated::
            Don't use

        Swap position index effectA to effectB
        """
        effectA.patch.swapEffects(effectA, effectB)
        self.dao.save(effectA.patch.bank)

    def _notify_change(self, patch, update_type, token=None):
        self.notificationController.notifyPatchUpdated(patch, update_type, token)
