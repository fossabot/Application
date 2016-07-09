# -*- coding: utf-8 -*-


class Param(object):
    __json = None
    effect = None

    def __init__(self, json, effect=None):
        self.__json = json
        self.effect = effect

    @property
    def json(self):
        return self.__json

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
           and self.json == other.json

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, key):
        return self.json[key]

    @property
    def value(self):
        return self["value"]

    @value.setter
    def value(self, value):
        self.__json["value"] = value

    @property
    def index(self):
        return self.effect.indexOfParam(self)
