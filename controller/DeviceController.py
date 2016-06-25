# -*- coding: utf-8 -*-
from controller.Controller import Controller
from lib.ModHostBinding.Host import Host
from lib.ModHostBinding.plugin.Lv2Plugin import Lv2Plugin


class DeviceController(Controller):
    '''
    Changes in the device (mod-host)
    '''

    currentPatch = {'plugins': []}
    host = None

    def configure(self):
        self.host = Host()

    def loadPatch(self, patch):
        #print("Removing plugins")
        for plugin in self.currentPatch['plugins']:
            self.host.remove(plugin)

        self.currentPatch = {'plugins': []}
        self.currentPatch['data'] = patch

        #print("Loading effects", patch["effects"])
        for effect in patch['effects']:
            plugin = Lv2Plugin(effect)
            self.host.add(plugin)
            self.currentPatch['plugins'].append(plugin)

        #print("connecting", patch["connections"])

    def toggleStatusEffect(self, effectIndex):
        print("Toggle status effect number:", effectIndex)

    def setEffectParam(self, effectIndex, param):
        print("Toggle status effect number:", effectIndex, param)
