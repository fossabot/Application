# -*- coding: utf-8 -*-


class Patch(object):
    json = None
    bank = None

    def __init__(self, json, bank=None):
        self.bank = bank
        self.json = json

    def __getitem__(self, key):
        return self.json[key]

    @property
    def effects(self):
        returned = []
        effects = self.json["effects"]

        for effectJson in effects:
            #effect = Effect(effectJson)
            returned.append(effectJson)

        return returned

    def addEffect(self, effect):
        self["effects"].append(effect.json)
        effect.patch = self
