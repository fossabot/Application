from glob import glob

from application.dao.database import Database
from pluginsmanager.util.persistence import Persistence


class BankDao(object):

    def __init__(self, data_path):
        self.data_path = data_path + 'banks/'

    def banks(self, system_effect):
        persistence = Persistence(system_effect)

        banks = []

        for file in glob(self.data_path + "*.json"):
            bank = persistence.read(Database.read(file))
            banks.append(bank)

        return sorted(banks, key=lambda b: b.index)

    def save(self, bank, index):
        bank.index = index
        Database.save(self._url(bank), bank.json)

    def delete(self, bank):
        Database.delete(self._url(bank))

    def _url(self, bank):
        return self.data_path + bank.original_name + ".json"
