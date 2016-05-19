from dao.BankDao import BankDao
from architecture.privatemethod import privatemethod

from model.Bank import Bank

from controller.Controller import Controller

class BanksController(Controller):
    banks = []

    def configure(self):
        self.banks = self.app.dao(BankDao).all

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

        return index
    
    @privatemethod
    def getNextBankIndex(self):
        try:
            lastBank = self.banks[len(self.banks) - 1]
            return lastBank.data["index"] + 1
        except IndexError as error:
            return 0

    def createPatch(self, bank, patch):
        bank.addPatch(patch)
        return len(bank.patches) - 1
    
    def addEffect(self, bank, indexPatch, effect):
        bank.addEffect(indexPatch, effect)
        return len(bank.getEffects(indexPatch)) - 1
    
    def updateBank(self, bank, data):
        index = bank.data["index"]
        bank.json.clear()
        bank.json.update(data)
        bank.json["index"] = index
        print("BanksController: Chamar internamente DeviceController para atualizar estado do dispositivo")
        
    def delete(self, bank):
        self.banks.delete(bank.data["index"])

        