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
    def createBank(self, banks, bank):
        bank = Bank(bank)
        banks.append(bank)
        return len(banks) - 1
    
    def createPatch(self, bank, patch):
        bank.addPatch(patch)
        return len(bank.patches) - 1
    
    def addEffect(self, bank, indexPatch, effect):
        bank.addEffect(indexPatch, effect)
        return len(bank.getEffects(indexPatch)) - 1
    
    def update(self, data, value):
        print("BanksController: Chamar internamente DeviceController para atualizar estado do dispositivo")
        data.clear()
        data.update(value)
        
    def delete(self, bank):
        self.banks.delete(bank.data["index"])

        