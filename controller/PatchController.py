# -*- coding: utf-8 -*-
from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController


class PatchController(Controller):

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)

    def createPatch(self, bank, patch):
        '''
        @return patch index
        '''
        bank.addPatch(patch)
        self.dao.save(bank)

        return len(bank.patches) - 1

    def updatePatch(self, bank, patchNumber, newPatchData):
        bank.patches[patchNumber] = newPatchData

        self.dao.save(bank)

        if self.currentController.isCurrent(bank, newPatchData):
            self.deviceController.loadPatch(newPatchData)

    def deletePatch(self, bank, patchNumber):
        patch = bank.patches[patchNumber]

        if self.currentController.isCurrent(bank, patch):
            self.currentController.toNextPatch()

        del bank.patches[patchNumber]

        self.dao.save(bank)
