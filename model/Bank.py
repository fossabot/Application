# -*- coding: utf-8 -*-
from architecture.BankError import BankError
from model.Patch import Patch


class Bank(object):
    __json = {}

    def __init__(self, json):
        self.validate(json)
        self.json = json

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

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
           and self.json == other.json

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def json(self):
        return self.__json

    @json.setter
    def json(self, value):
        self.__json = dict(value)
        #FIXME - Add validation

    @property
    def index(self):
        try:
            return self["index"]
        except KeyError:
            return -1

    @index.setter
    def index(self, value):
        self.json["index"] = value

    @property
    def patches(self):
        returned = []

        for patchJson in self['patches']:
            returned.append(Patch(patchJson, self))

        return returned

    # ==================================
    # Methods
    # ==================================
    def addPatch(self, patch):
        self['patches'].append(patch.json)
        patch.bank = self

    def indexOfPatch(self, patch):
        return self['patches'].index(patch.json)

    def swapPatches(self, patchA, patchB):
        if patchA.bank != self or patchB.bank != self:
            raise BankError("patchA or patchB aren't of this bank")

        indexA = patchA.index
        indexB = patchB.index

        patches = self.json['patches']

        patches[indexA], patches[indexB] = patches[indexB], patches[indexA]
