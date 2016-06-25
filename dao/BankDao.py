# -*- coding: utf-8 -*-
import glob

from dao.DataBank import DataBank
from architecture.privatemethod import privatemethod

from model.Bank import Bank
from model.Banks import Banks


class BankDao(object):
    dataPath = ""

    def __init__(self, dataPath):
        self.dataPath = dataPath + 'banks/'

    @property
    def all(self):
        return self.readBanks(self.dataPath)

    @privatemethod
    def readBanks(self, dataPath):
        banks = Banks()

        for file in glob.glob(dataPath + "*.json"):
            bank = Bank(DataBank.read(file))
            banks.append(bank)

        return banks

    def save(self, bank):
        DataBank.save(self.url(bank), bank.json)

    def delete(self, bank):
        DataBank.delete(self.url(bank))

    @privatemethod
    def url(self, bank):
        return self.dataPath + bank.data["name"] + ".json"
