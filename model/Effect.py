# -*- coding: utf-8 -*-


class Effect(object):
    json = None
    patch = None

    def __init__(self, json, patch=None):
        self.json = json
        self.patch = patch

    @property
    def params(self):
        return self.json["ports"]["control"]["input"]

    def __getitem__(self, key):
        return self.json[key]
