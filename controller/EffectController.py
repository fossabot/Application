# -*- coding: utf-8 -*-
from architecture.EffectException import EffectException
from architecture.privatemethod import privatemethod

from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController

from controller.PluginsController import PluginsController

from model.Effect import Effect
from model.UpdatesObserver import UpdateType


class EffectController(Controller):
    dao = None
    currentController = None
    deviceController = None
    pluginsController = None

    def configure(self):
        from controller.CurrentController import CurrentController
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)
        self.pluginsController = self.app.controller(PluginsController)

    def createEffect(self, patch, uri):
        """
        @return effect index
        """
        try:
            plugin = self.pluginsController.plugins[uri]
        except KeyError:
            raise EffectException('Undefined plugin uri ' + uri)

        effect = self.prepareEffect(plugin)
        patch.addEffect(effect)

        self.update(patch)
        self.notifyChange(effect, UpdateType.CREATED)

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

        del patch['effects'][effect.index]

        self.update(patch)
        self.notifyChange(effect, UpdateType.DELETED)

    def toggleStatus(self, effect):
        effect.json["status"] = not effect.status
        patch = effect.patch

        self.update(patch)
        self.notificationController.notifyEffectStatusToggled(effect)

    @privatemethod
    def update(self, patch):
        self.dao.save(patch.bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.loadPatch(patch)

    @privatemethod
    def notifyChange(self, effect, updateType):
        self.notificationController.notifyEffectUpdated(effect, updateType)
