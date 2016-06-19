from dao.BankDao import BankDao

from model.Bank import Bank

from controller.Controller import Controller


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

    def createBank(self, bank):
        bankModel = Bank(bank)

        self.banks.append(bankModel)
        self.dao.save(bankModel)

        return bankModel.index

    def updateBank(self, bank, data):
        self.dao.delete(bank)
        bank.data = data
        self.dao.save(bank)

        print("BanksController: Chamar internamente DeviceController \
               para atualizar estado do dispositivo se for o atual")

    def deleteBank(self, bank):
        self.banks.delete(bank.data["index"])
        self.dao.delete(bank)
        print("BanksController: Chamar internamente DeviceController para \
              atualizar estado do dispositivo se for o atual")
