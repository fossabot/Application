# -*- coding: utf-8 -*-
from architecture.privatemethod import privatemethod

from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController

from model.Patch import Patch
from model.UpdatesObserver import UpdateType


class PatchController(Controller):
    dao = None
    currentController = None
    deviceController = None
    notificationController = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def createPatch(self, bank, patchJson):
        """
        @return patch index
        """
        patch = Patch(patchJson)
        bank.addPatch(patch)
        self.dao.save(bank)

        self.notifyChange(patch, UpdateType.CREATED)

        return len(bank.patches) - 1

    def updatePatch(self, patch, newPatchData):
        patch.json = newPatchData

        self.dao.save(patch.bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.loadPatch(patch)

        self.notifyChange(patch, UpdateType.UPDATED)

    def deletePatch(self, patch):
        bank = patch.bank

        if self.currentController.isCurrentPatch(patch):
            self.currentController.toNextPatch()

        self.notifyChange(patch, UpdateType.DELETED)
        del bank['patches'][patch.index]

        self.dao.save(bank)

    @privatemethod
    def notifyChange(self, patch, updateType):
        self.notificationController.notifyPatchUpdated(patch, updateType)
