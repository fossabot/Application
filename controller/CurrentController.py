# -*- coding: utf-8 -*-

from architecture.privatemethod import privatemethod

from controller.Controller import Controller
from controller.BanksController import BanksController
from controller.DeviceController import DeviceController
from controller.EffectController import EffectController
from controller.NotificationController import NotificationController
from controller.ParamController import ParamController

from dao.CurrentDao import CurrentDao


class CurrentController(Controller):
    bankNumber = 0
    patchNumber = 0

    deviceController = None
    banksController = None
    notificationController = None

    def configure(self):
        data = self.app.dao(CurrentDao).load()
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
        return self.currentBank.patches[self.patchNumber]

    @property
    def currentBank(self):
        return self.banksController.banks[self.bankNumber]

    # ************************
    # Persistance
    # ************************
    @privatemethod
    def saveCurrent(self):
        print("Necessary implements: SAVING", self.bankNumber, self.patchNumber)

    # ************************
    # Effect
    # ************************
    def toggleStatusEffect(self, effectIndex):
        effect = self.currentPatch.effects[effectIndex]
        self.effectController.toggleStatus(effect)

    def setEffectParam(self, effectIndex, paramIndex, newValue):
        effect = self.currentPatch.effects[effectIndex]
        param = effect.params[paramIndex]

        self.paramController.updateValue(param, newValue)

    # ************************
    # Get of Current
    # ************************
    def isCurrentBank(self, bank):
        return bank.index == self.bankNumber

    def isCurrentPatch(self, patch):
        return self.isCurrentBank(patch.bank) and self.currentPatch == patch

    # ************************
    # Set Current Patch/Bank
    # ************************
    def toBeforePatch(self):
        beforePatchNumber = self.patchNumber - 1
        if beforePatchNumber == -1:
            beforePatchNumber = len(self.currentBank.patches) - 1

        self.setPatch(beforePatchNumber)

    def toNextPatch(self):
        nextPatchNumber = self.patchNumber + 1
        if nextPatchNumber == len(self.currentBank.patches):
            nextPatchNumber = 0

        self.setPatch(nextPatchNumber)

    def setPatch(self, patchNumber):
        if self.patchNumber == patchNumber:
            return

        self.setCurrent(self.bankNumber, patchNumber)

    def toBeforeBank(self):
        banks = self.banksController.banks.all
        position = banks.index(self.currentBank)

        before = position - 1
        if before == -1:
            before = len(banks) - 1

        beforeBankIndex = banks[before].index

        self.setBank(beforeBankIndex)

    def toNextBank(self):
        banks = self.banksController.banks.all
        position = banks.index(self.currentBank)

        nextBankIndex = position + 1
        if nextBankIndex == len(banks):
            nextBankIndex = 0

        nextBank = banks[nextBankIndex].index

        self.setBank(nextBank)

    def setBank(self, bankNumber):
        if self.bankNumber == bankNumber:
            return

        self.setCurrent(bankNumber, 0)

    @privatemethod
    def setCurrent(self, bankNumber, patchNumber):
        self.loadDevicePatch(  # throwable. need be first
            bankNumber,
            patchNumber
        )
        self.bankNumber = bankNumber
        self.patchNumber = patchNumber
        self.saveCurrent()

        self.notificationController.notifyCurrentPatchChange(self.currentPatch)

    @privatemethod
    def loadDevicePatch(self, bankNumber, patchNumber):
        bank = self.banksController.banks[bankNumber]
        patch = bank.patches[patchNumber]

        self.deviceController.loadPatch(patch)
