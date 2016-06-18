# -*- coding: utf-8 -*-
from controller.Controller import Controller
from util.ModHostBinding.Host import Host
from util.ModHostBinding.plugin.Lv2Plugin import Lv2Plugin


class DeviceController(Controller):
    '''
    Changes in the device (mod-host)
    '''

    currentPatch = {'plugins': []}
    host = None

    def configure(self):
        self.host = Host()

    def loadPatch(self, patch):
        print("Removing plugins")
        for plugin in self.currentPatch['plugins']:
            self.host.remove(plugin)

        self.currentPatch = {'plugins': []}
        self.currentPatch['data'] = patch

        print("Loading effects", patch["effects"])
        for effect in patch['effects']:
            plugin = Lv2Plugin(effect)
            self.host.add(plugin)
            self.currentPatch['plugins'].append(plugin)

        print("connecting", patch["connections"])

    def toggleStatusEffect(self, effect):
        print("Toggle status effect number:", effect)

    def setEffectParam(self, effect, param):
        print("Toggle status effect number:", effect, param)
