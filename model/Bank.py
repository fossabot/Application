# -*- coding: utf-8 -*-
from architecture.privatemethod import privatemethod
from architecture.BankError import BankError


class Bank(object):
    _data = {}

    def __init__(self, data):
        self._data = data

    def validate(self, data):
        if 'patches' not in data:
            raise BankError('invalid bank structure')
        elif len(data['patches']) == 0:
            raise BankError('Bank no contains any patch')

    # ==================================
    # Property
    # ==================================

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self.validate(value)
        self._data = value

    @property
    def json(self):
        return self.data

    @json.setter
    def setJson(self, value):
        self.data = value

    @property
    def patches(self):
        return self.data["patches"]

    @property
    def index(self):
        try:
            return self.data["index"]
        except KeyError:
            return -1

    @index.setter
    def index(self, value):
        self.data["index"] = value

    # ==================================
    # Facade
    # ==================================

    def getParam(self, patchIndex, effectIndex, paramIndex):
        params = self.getParams(patchIndex, effectIndex)
        return self.get(params, paramIndex)

    def getParams(self, patchIndex, effectIndex):
        return self.getEffect(patchIndex, effectIndex)['ports']['control']['input']

    def addEffect(self, patch, effect):
        patch["effects"].append(effect)

    def getEffect(self, patchIndex, effectIndex):
        effects = self.getEffects(patchIndex)
        return self.get(effects, effectIndex)

    def getEffects(self, patchIndex):
        return self.getPatch(patchIndex)["effects"]

    def getPatch(self, patchIndex):
        return self.get(self.patches, patchIndex)

    def addPatch(self, patch):
        self.patches.append(patch)

    # ==================================
    # Private
    # ==================================

    @privatemethod
    def get(self, collection, index):
        try:
            return collection[index]
        except IndexError:
            raise IndexError("Element not found")
