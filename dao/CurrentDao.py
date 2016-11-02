# -*- coding: utf-8 -*-
from dao.DataBank import DataBank


class CurrentDao(object):

    def __init__(self, data_path):
        self.data_path = data_path + 'current/'

    def load(self):
        return self._read_file()

    def save(self, bank_index, patch_index):
        json = {
            "bank": bank_index,
            "patch": patch_index
        }

        DataBank.save(self._url(), json)

    def _read_file(self):
        return DataBank.read(self._url())

    def _url(self):
        return self.data_path + "current.json"
