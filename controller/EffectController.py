# -*- coding: utf-8 -*-
from architecture.EffectException import EffectException
from architecture.privatemethod import privatemethod

from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.PluginsController import PluginsController


class EffectController(Controller):

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.pluginsController = self.app.controller(PluginsController)

    def createEffect(self, bank, patch, uri):
        '''
        @return effect index
        '''
        try:
            plugin = self.pluginsController.plugins[uri]
        except KeyError:
            raise EffectException('Undefined plugin uri ' + uri)

        effect = self.prepareEffect(plugin)
        bank.addEffect(patch, effect)

        self.update(bank, patch)

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
        
        return effect

    def deleteEffect(self, bank, patch, effectIndex):
        del patch['effects'][effectIndex]

        self.update(bank, patch)

    @privatemethod
    def update(self, bank, patch):
        self.dao.save(bank)

        if self.currentController.isCurrent(bank, patch):
            self.deviceController.loadPatch(
                self.currentController.getCurrentPatch()
            )
