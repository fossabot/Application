# -*- coding: utf-8 -*-
from dao.DataBank import DataBank
from architecture.privatemethod import privatemethod


class CurrentDao(object):
    dataPath = ""

    def __init__(self, dataPath):
        self.dataPath = dataPath + 'current/'

    def load(self):
        return self.readFile()

    def save(self, bankIndex, patchIndex):
        json = {
            "bank": bankIndex,
            "patch": patchIndex
        }

        DataBank.save(self.url(), json)

    @privatemethod
    def readFile(self):
        return DataBank.read(self.url())

    @privatemethod
    def url(self):
        return self.dataPath + "current.json"