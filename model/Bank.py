# -*- coding: utf-8 -*-
from architecture.BankError import BankError
from model.Patch import Patch


class Bank(object):
    _data = {}

    def __init__(self, json):
        self._data = json
        self.validate(json)

    #FIXME - Json Schema
    def validate(self, data):
        if 'patches' not in data:
            raise BankError('invalid bank structure')
        elif len(data['patches']) == 0:
            raise BankError('Bank no contains any patch')

    # ==================================
    # Property
    # ==================================
    def __getitem__(self, key):
        return self.json[key]

    @property
    def json(self):
        return self._data

    @json.setter
    def setJson(self, value):
        self._data = value
        #FIXME - Add validation

    @property
    def patches(self):
        returned = []

        for patchJson in self["patches"]:
            returned.append(Patch(self, patchJson))

        return returned

    @property
    def index(self):
        try:
            return self["index"]
        except KeyError:
            return -1

    @index.setter
    def index(self, value):
        self.json["index"] = value

    # ==================================
    # Methods
    # ==================================
    def addPatch(self, patch):
        self["patches"].append(patch.json)
        patch.bank = self
