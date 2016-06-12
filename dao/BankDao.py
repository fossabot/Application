import glob

from dao.DataBank import DataBank
from architecture.privatemethod import privatemethod

from model.Bank import Bank
from model.Banks import Banks

class BankDao:
    dataPath = ""

    def __init__(self, dataPath):
        self.dataPath = dataPath + 'banks/'

    @property
    def all(self):
        return self.readBanks(self.dataPath)

    @privatemethod
    def readBanks(self, dataPath):
        banks = Banks([])

        for file in glob.glob(dataPath + "*.json"):
            bank = Bank(DataBank.read(file))
            banks.insert(bank.data["index"], bank)

        return banks

    def save(self, bank):
        DataBank.save(self.url(bank), bank.json)

    def delete(self, bank):
        DataBank.delete(self.url(bank))

    @privatemethod
    def url(self, bank):
        return self.dataPath + "/" + bank.data["name"] + ".json"

    '''
    @my_attribute.setter
    def my_attribute(self, value):
        # Do something if you want
        self._my_attribute = value
    '''

