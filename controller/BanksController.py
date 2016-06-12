from dao.BankDao import BankDao
from architecture.privatemethod import privatemethod

from model.Bank import Bank

from controller.Controller import Controller


class BanksController(Controller):
    '''
    For get bank/patch/effect of patch/param, use self.banks
    '''
    banks = []

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.dao.all

        from controller.CurrentController import CurrentController  # Cyclic dependece
        self.currentController = self.app.controller(CurrentController)

    '''
    ***********************************
    Data CRUD
    ***********************************
    '''
    def createBank(self, bank):
        index = self.getNextBankIndex()

        bank["index"] = index

        bank = Bank(bank)
        self.banks.append(bank)

        self.dao.save(bank)

        self.currentController.setBank(index)
        return index

    @privatemethod
    def getNextBankIndex(self):
        try:
            lastBank = self.banks[len(self.banks) - 1]
            return lastBank.data["index"] + 1
        except IndexError:
            return 0

    def updateBank(self, bank, data):
        self.dao.delete(bank)

        index = bank.data["index"]
        bank.json.clear()
        bank.json.update(data)
        bank.json["index"] = index

        self.dao.save(bank)

        print("BanksController: Chamar internamente DeviceController para atualizar estado do dispositivo")

    def deleteBank(self, bank):
        self.banks.delete(bank.data["index"])
        self.dao.delete(bank)
        print("BanksController: Chamar internamente DeviceController para atualizar estado do dispositivo")

    def createPatch(self, bank, patch):
        bank.addPatch(patch)
        print("Dao: salvar")
        print("Current: Chamar CurrentController para atualizar estado do dispositivo")
        return len(bank.patches) - 1

    def addEffect(self, bank, indexPatch, effect):
        bank.addEffect(indexPatch, effect)
        print("BanksController: Chamar internamente DeviceController para atualizar estado do dispositivo")
        return len(bank.getEffects(indexPatch)) - 1
