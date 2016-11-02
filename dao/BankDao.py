# -*- coding: utf-8 -*-
import glob

from dao.DataBank import DataBank

from model.Bank import Bank
from model.Banks import Banks


class BankDao(object):

    def __init__(self, data_path):
        self.data_path = data_path + 'banks/'

    @property
    def all(self):
        return self._read_banks(self.data_path)

    def _read_banks(self, data_path):
        banks = Banks()

        for file in glob.glob(data_path + "*.json"):
            bank = Bank(DataBank.read(file))
            banks.append(bank)

        return banks

    def save(self, bank):
        DataBank.save(self._url(bank), bank.json)

    def delete(self, bank):
        DataBank.delete(self._url(bank))

    def _url(self, bank):
        return self.data_path + bank["name"] + ".json"
