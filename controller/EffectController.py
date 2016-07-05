# -*- coding: utf-8 -*-
from architecture.EffectException import EffectException
from architecture.privatemethod import privatemethod

from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.PluginsController import PluginsController
from model.Effect import Effect


class EffectController(Controller):
    dao = None
    currentController = None
    deviceController = None
    pluginsController = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.pluginsController = self.app.controller(PluginsController)

    def createEffect(self, patch, uri):
        """
        @return effect index
        """
        try:
            plugin = self.pluginsController.plugins[uri]
        except KeyError:
            raise EffectException('Undefined plugin uri ' + uri)

        patch.addEffect(self.prepareEffect(plugin))

        self.update(patch)

        return len(patch['effects']) - 1

    @privatemethod
    def prepareEffect(self, plugin):
        effect = dict()

        effect['uri'] = plugin['uri']

        effect['name'] = plugin['name']
        effect['label'] = plugin['label']
        effect['author'] = plugin['author']

        effect['ports'] = dict(plugin['ports'])
        effect['status'] = True

        effect = self.preparePorts(effect)

        return Effect(effect)

    @privatemethod
    def preparePorts(self, effect):
        for param in effect['ports']['control']['input']:
            param['value'] = param['ranges']['default']
        
        return effect

    def deleteEffect(self, effect):
        patch = effect.patch

        effectIndex = effect.patch.indexOfEffect(effect)
        del patch['effects'][effectIndex]

        self.update(patch)

    @privatemethod
    def update(self, patch):
        self.dao.save(patch.bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.loadPatch(patch)
