# -*- coding: utf-8 -*-
from dao.DataBank import DataBank


class ComponentDao(object):

    def __init__(self, data_path):
        self.data_path = data_path + 'components/'

    def load(self):
        return self._read_file()

    def save(self, data):
        DataBank.save(self._url(), data)

    def _read_file(self):
        return DataBank.read(self._url())

    def _url(self):
        return self.data_path + "component.json"
