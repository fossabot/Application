# -*- coding: utf-8 -*-
from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController

from model.Patch import Patch


class PatchController(Controller):
    dao = None
    currentController = None
    deviceController = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)

    def createPatch(self, bank, patchJson):
        """
        @return patch index
        """
        bank.addPatch(Patch(patchJson))
        self.dao.save(bank)

        return len(bank.patches) - 1

    def updatePatch(self, patch, newPatchData):
        patch.json = dict(newPatchData) #FIXME Referecen problem

        self.dao.save(patch.bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.loadPatch(patch)

    def deletePatch(self, patch):
        bank = patch.bank
        patchNumber = bank.indexOfPatch(patch)

        if self.currentController.isCurrentPatch(patch):
            self.currentController.toNextPatch()

        del bank['patches'][patchNumber]

        self.dao.save(bank)
