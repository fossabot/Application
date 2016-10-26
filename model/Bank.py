# -*- coding: utf-8 -*-
from architecture.BankError import BankError
from model.Patch import Patch


class Bank(object):
    """
    Bank is a data structure that contains :class:`Patch`. It's useful
    for group common patches, like "Patches will be used in
    the Sunday show"
    """

    __json = {}

    def __init__(self, json):
        self.validate(json)
        self.json = json

    def validate(self, data):
        """
        Validate the data, raising if a error is dettected.
        The data will represents the :class:`Bank` information in
        dict mode.

        .. todo:: Add json Schema verification

        :param dict data: Bank definition in ``dict``
        """
        if 'patches' not in data:
            raise BankError('invalid bank structure')
        elif len(data['patches']) == 0:
            raise BankError('Bank no contains any patch')

    # ==================================
    # Property
    # ==================================
    def __getitem__(self, key):
        """
        :param string key: Property key
        :return: Returns a Bank property
        """
        return self.json[key]

    def __eq__(self, another):
        """
        Compare this bank with another Bank if they are equals

        :param Bank another: Other bank that be comparable
        :return bool: This bank is equals to another bank?
        """
        return isinstance(another, self.__class__) \
           and self.json == another.json

    def __ne__(self, another):
        """
        Compare this bank with another Bank if they are't equals

        :param Bank another: Other bank that be comparable
        :return bool: This bank is not equals to another bank?
        """
        return not self.__eq__(another)

    @property
    def json(self):
        """
        Get a json representation of this bank

        :return dict: json representation
        """
        return self.__json

    @json.setter
    def json(self, value):
        """
        Change this bank by a json representation

        .. note::
            Caution, please

        .. todo:: Add validation

        :param string value: Json representation
        """
        self.__json = dict(value)

    @property
    def index(self):
        """
        :return int: Bank index. -1 if it not persisted
        """
        try:
            return self["index"]
        except KeyError:
            return -1

    @index.setter
    def index(self, value):
        """
        Set the :class:`Bank` index.

        :param int value: New bank index
        """
        self.json["index"] = value

    @property
    def patches(self):
        """
        Returns all :class:`Patch` of this bank
        """
        returned = []

        for patchJson in self['patches']:
            returned.append(Patch(patchJson, self))

        return returned

    # ==================================
    # Methods
    # ==================================
    def addPatch(self, patch):
        """
        Add a :class:`Patch` in this bank

        :param Patch patch: Patch that will be added
        """
        self['patches'].append(patch.json)
        patch.bank = self

    def indexOfPatch(self, patch):
        """
        .. deprecated::
            Use :func:`index` :class:`Patch` attribute instead.

        :param Patch patch:
        :return: Index of the patch
        """
        return self['patches'].index(patch.json)

    def swapPatches(self, patchA, patchB):
        """
        .. deprecated:: ever
            Don't use
        """
        if patchA.bank != self or patchB.bank != self:
            raise BankError("patchA or patchB aren't of this bank")

        indexA = patchA.index
        indexB = patchB.index

        patches = self.json['patches']

        patches[indexA], patches[indexB] = patches[indexB], patches[indexA]
