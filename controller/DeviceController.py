# -*- coding: utf-8 -*-
from controller.Controller import Controller
from lib.ModHostBinding.Host import Host
from lib.ModHostBinding.plugin.Lv2Plugin import Lv2Plugin


class DeviceController(Controller):
    """
    Apply changes in the device (mod-host)
    """

    currentPatch = {'plugins': []}
    address = 'localhost'
    host = None

    def configure(self):
        self.host = Host(self.address)

    def loadPatch(self, patch):
        print("Removing old plugins")
        self.removeOldPlugins()

        self.plugins = []

        #print("Loading effects", patch["effects"])
        print("Loading effects")
        self.loadEffectsOf(patch)

        print("connecting", patch["connections"])
        self.autoConnect()

    def removeOldPlugins(self):
        for plugin in self.plugins:
            self.host.remove(plugin)

    def loadEffectsOf(self, patch):
        for effect in patch.effects:
            plugin = Lv2Plugin(effect.json)
            self.host.add(plugin)
            self.plugins.append(plugin)

            print("Loading params of", effect['name'])
            self.loadParamsOf(effect)
            self.setStatusEffect(effect)

    def loadParamsOf(self, effect):
        for param in effect.params:
            self.updateParamValue(param)

    def autoConnect(self):
        if len(self.plugins) == 0:
            return

        first = self.plugins[0]
        last = self.plugins[-1]

        self.host.connect_input_in(first)

        before = first
        for plugin in self.plugins[1:]:
            self.host.connect(before, plugin)
            before = plugin

        self.host.connect_on_output(last, 1)
        self.host.connect_on_output(last, 2)

    @property
    def plugins(self):
        return self.currentPatch['plugins']

    @plugins.setter
    def plugins(self, plugins):
        self.currentPatch['plugins'] = plugins

    def setStatusEffect(self, effect):
        self.host.set_status(self.pluginOfEffect(effect))

    def updateParamValue(self, param):
        self.host.set_param_value(self.pluginOfEffect(param.effect), param)

    def pluginOfEffect(self, effect):
        return self.plugins[effect.index]
