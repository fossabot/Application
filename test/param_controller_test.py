# -*- coding: utf-8 -*-
import unittest

from architecture.privatemethod import privatemethod

from Application import ApplicationSingleton

from controller.CurrentController import CurrentController
from controller.EffectController import EffectController
from controller.ParamController import ParamController
from controller.PluginsController import PluginsController


class ParamControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()

    def setUp(self):
        self.controller = self.get_controller(ParamController)
        self.effectController = self.get_controller(EffectController)
        self.pluginsController = self.get_controller(PluginsController)
        self.currentController = self.get_controller(CurrentController)

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

        self.currentBank = self.currentController.currentBank
        self.currentPatch = self.currentController.currentPatch

    @privatemethod
    def get_controller(self, controller):
        return ParamControllerTest.application.controller(controller)

    def test_update_value(self):
        uri = 'http://guitarix.sourceforge.net/plugins/gx_reverb_stereo#_reverb_stereo'

        effectIndex = self.effectController.createEffect(self.currentPatch, uri)

        effect = self.currentPatch.effects[effectIndex]
        param = effect.params[0]

        ranges = param['ranges']
        newValue = (ranges['maximum'] + ranges['minimum']) / 2
        self.controller.updateValue(effect, param, newValue)

        self.assertEqual(param['value'], newValue)

        self.effectController.deleteEffect(effect)
