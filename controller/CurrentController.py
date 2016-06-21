# -*- coding: utf-8 -*-

from architecture.privatemethod import privatemethod

from controller.Controller import Controller
from controller.BanksController import BanksController
from controller.DeviceController import DeviceController

from dao.CurrentDao import CurrentDao


class CurrentController(Controller):
    bankNumber = 0
    patchNumber = 0

    def configure(self):
        data = self.app.dao(CurrentDao).load()
        self.bankNumber = data["bank"]
        self.patchNumber = data["patch"]

        self.deviceController = self.app.controller(DeviceController)
        self.banksController = self.app.controller(BanksController)

    # ************************
    # Persistance
    # ************************
    @privatemethod
    def saveCurrent(self):
        print("Necessary implements: SAVING", self.bankNumber, self.patchNumber)

    # ************************
    # Effect
    # ************************
    def toggleStatusEffect(self, effectNumber):
        effect = self.getEffectOfCurrentPatch(effectNumber)
        effect["active"] = not effect["active"]

        self.deviceController.toggleStatusEffect(effectNumber)
        self.saveCurrent()

    def setEffectParam(self, effectNumber, param):
        self.deviceController.setEffectParam(effectNumber, param)
        self.saveCurrent()

    # ************************
    # Get of Current
    # ************************
    def isCurrent(self, bank, patch):
        return bank.index == self.bankNumber \
           and self.getCurrentPatch() == patch

    # ************************
    # Get of Current
    # ************************
    def getEffectOfCurrentPatch(self, effectNumber):
        patch = self.getCurrentPatch()
        try:
            return patch["effects"][effectNumber]
        except IndexError:
            raise IndexError("Element not found")

    def getCurrentPatch(self):
        return self.getCurrentBank().getPatch(self.patchNumber)

    def getCurrentBank(self):
        return self.banksController.banks[self.bankNumber]

    # ************************
    # Set Current Patch/Bank
    # ************************
    def beforePatch(self):
        before = self.patchNumber - 1
        if before == -1:
            before = len(self.getCurrentBank().patches) - 1
        
        self.setPatch(self.patchNumber)

    def nextPatch(self):
        next = self.patchNumber+1
        if next == len(self.getCurrentBank().patches):
            next = 0
        
        self.setPatch(next)

    def setPatch(self, patchNumber):
        if self.patchNumber == patchNumber:
            return

        self.setCurrent(self.bankNumber, patchNumber)

    def beforeBank(self):
        banks = self.banksController.banks.all
        position = banks.index(self.getCurrentBank())
        
        before = position - 1
        if before == -1:
            before = len(banks) - 1

        beforeBankIndex = banks[before].index
        
        self.setBank(beforeBankIndex)

    def nextBank(self):
        banks = self.banksController.banks.all
        position = banks.index(self.getCurrentBank())
        
        next = position + 1
        if next == len(banks):
            next = 0

        nextBankIndex = banks[next].index

        self.setBank(nextBankIndex)

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

    @privatemethod
    def loadDevicePatch(self, bankNumber, patchNumber):
        bank = self.banksController.banks[bankNumber]
        patch = bank.getPatch(patchNumber)

        self.deviceController.loadPatch(patch)
