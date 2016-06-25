from dao.BankDao import BankDao

from model.Bank import Bank

from controller.Controller import Controller
from controller.DeviceController import DeviceController


class BanksController(Controller):
    '''
    For get bank/patch/effect of patch/param, use self.banks
    '''
    banks = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.dao.all

        # To fix Cyclic dependece
        from controller.CurrentController import CurrentController
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)

    def createBank(self, bank):
        bankModel = Bank(bank)

        self.banks.append(bankModel)
        self.dao.save(bankModel)

        return bankModel.index

    def updateBank(self, bank, data):
        self.dao.delete(bank)
        bank.data = dict(data)

        self.dao.save(bank)
        if bank == self.currentController.getCurrentBank():
            self.deviceController.loadPatch(
                self.currentController.getCurrentPatch()
            )

    def deleteBank(self, bank):
        if bank == self.currentController.getCurrentBank():
            self.currentController.toNextBank()

        del self.banks[bank.index]
        self.dao.delete(bank)
