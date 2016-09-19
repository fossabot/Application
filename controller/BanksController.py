# -*- coding: utf-8 -*-
from architecture.privatemethod import privatemethod

from dao.BankDao import BankDao

from model.Bank import Bank
from model.UpdatesObserver import UpdateType

from controller.Controller import Controller
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController


class BanksController(Controller):
    banks = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.dao.all

        # To fix Cyclic dependece
        from controller.CurrentController import CurrentController
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def createBank(self, bank, token=None):
        """
        :param bank: dict
        :param token: Request token identifier
        :return: bank index
        """
        bankModel = Bank(bank)

        self.banks.append(bankModel)
        self.dao.save(bankModel)
        self.notifyChange(bankModel, UpdateType.CREATED, token)

        return bankModel.index

    def updateBank(self, bank, data, token=None):
        self.dao.delete(bank)
        bank.json = data

        self.dao.save(bank)
        if self.currentController.isCurrentBank(bank):
            currentPatch = self.currentController.currentPatch
            self.deviceController.loadPatch(currentPatch)

        self.notifyChange(bank, UpdateType.UPDATED, token)

    def deleteBank(self, bank, token=None):
        if bank == self.currentController.currentBank:
            self.currentController.toNextBank()

        del self.banks[bank.index]
        self.dao.delete(bank)

        self.notifyChange(bank, UpdateType.DELETED, token)

    def swapBanks(self, bankA, bankB, token=None):
        self.banks.swap(bankA, bankB)

        self.dao.save(bankA)
        self.dao.save(bankB)

        self.notifyChange(bankA, UpdateType.UPDATED, token)
        self.notifyChange(bankB, UpdateType.UPDATED, token)

    def swapPatches(self, patchA, patchB):
        patchA.bank.swapPatches(patchA, patchB)
        self.dao.save(patchA.bank)

    @privatemethod
    def notifyChange(self, bank, update_type, token=None):
        self.notificationController.notifyBankUpdate(bank, update_type, token)
