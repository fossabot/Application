# -*- coding: utf-8 -*-
from architecture.EffectException import EffectException

from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController

from controller.PluginsController import PluginsController

from model.Effect import Effect
from model.UpdatesObserver import UpdateType


class EffectController(Controller):
    """
    Manage :class:`Effect`, creating new, deleting or changing status.
    """
    dao = None
    currentController = None
    deviceController = None
    pluginsController = None
    notificationController = None

    def configure(self):
        from controller.CurrentController import CurrentController
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)
        self.pluginsController = self.app.controller(PluginsController)

    def createEffect(self, patch, uri):
        """
        Add an :class:`Effect` in a :class:`Patch`

        :param Patch patch: Patch that will be added effect
        :param string uri: Effect plugin LV2 uri identifier
        :return int: Index of effect created
        """
        try:
            plugin = self.pluginsController.plugins[uri]
        except KeyError:
            raise EffectException('Undefined plugin uri ' + uri)

        effect = self._prepare_effect(plugin)
        patch.addEffect(effect)

        self._update(patch)
        self._notify_change(effect, UpdateType.CREATED)

        return len(patch['effects']) - 1

    def _prepare_effect(self, plugin):
        effect = dict()

        effect['uri'] = plugin['uri']

        effect['name'] = plugin['name']
        effect['label'] = plugin['label']
        effect['author'] = plugin['author']

        effect['ports'] = dict(plugin['ports'])
        effect['status'] = True

        effect = self._prepare_ports(effect)

        return Effect(effect)

    def _prepare_ports(self, effect):
        for param in effect['ports']['control']['input']:
            param['value'] = param['ranges']['default']

        return effect

    def deleteEffect(self, effect):
        """
        Remove an :class:`Effect` instance in your :class:`Patch`

        :param Effect effect: Effect will be removed
        """
        patch = effect.patch

        if patch is None:
            raise EffectException("Effect not contains a patch")

        self._notify_change(effect, UpdateType.DELETED)
        patch.deleteEffect(effect)

        self._update(patch)

    def toggleStatus(self, effect, token=None):
        """
        Toggle the effect status: ``status = not effect.status``

        :param Effect effect: Effect will be toggled your status
        :param string token: Request token identifier
        """
        effect.json["status"] = not effect.status
        patch = effect.patch

        self._update(patch)
        self.notificationController.notifyEffectStatusToggled(effect, token)

    def _update(self, patch):
        self.dao.save(patch.bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.loadPatch(patch)

    def _notify_change(self, effect, updateType):
        self.notificationController.notifyEffectUpdated(effect, updateType)

    def connect(self, effectOutput, output, effectInput, input):
        """
        Connect the output of effectOutput to input of effectInput::

        >>> patch = currentController.currentPatch

        >>> effectOutput = patch.effects[0]
        >>> effectInput = patch.effects[1]

        >>> output = effectOutput.outputs[0]
        >>> input = effectOutput.inputs[1]

        >>> effectController.connect(effectOutput, output, effectInput, input)

        :param Effect effectOutput: Effect that the output port audio will be connect with input port audio
        :param dict output: Output port information of effectOutput
        :param Effect effectInput:Effect that the input port audio will be connect with output port audio
        :param dict input: Input port information of effectInput
        """
        if effectOutput.patch != effectInput.patch:
            raise EffectException('Effect output and effect input are\'nt of the same patch')

        patch = effectOutput.patch
        patch.connect(effectOutput, output, effectInput, input)
