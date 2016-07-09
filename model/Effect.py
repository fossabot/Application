# -*- coding: utf-8 -*-
from model.Param import Param


class Effect(object):
    __json = None
    patch = None

    def __init__(self, json, patch=None):
        self.__json = json
        self.patch = patch

    @property
    def json(self):
        return self.__json

    @json.setter
    def json(self, value):
        """
        Set the json updates the values of the original reference
        (passed in constructor) for reflects changes in bank structure (of your patch)
        """
        self.__json.clear()
        self.__json.update(value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
           and self.json == other.json

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, key):
        return self.json[key]

    @property
    def index(self):
        return self.patch.indexOfEffect(self)

    @property
    def params(self):
        returned = []

        for param in self["ports"]["control"]["input"]:
            returned.append(Param(param, self))

        return returned

    @property
    def status(self):
        return self['status']

    def indexOfParam(self, param):
        return self["ports"]["control"]["input"].index(param.json)
