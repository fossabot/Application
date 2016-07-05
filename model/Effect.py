# -*- coding: utf-8 -*-


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
        self.__json.clear()
        self.__json.update(value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
           and self.json == other.json

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def params(self):
        return self.json["ports"]["control"]["input"]

    def __getitem__(self, key):
        return self.json[key]
