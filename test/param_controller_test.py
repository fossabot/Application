# -*- coding: utf-8 -*-
import unittest

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
        print("Loaded Application")

    def setUp(self):
        self.controller = ParamControllerTest.application.controller(
            ParamController
        )

        self.effectController = ParamControllerTest.application.controller(
            EffectController
        )

        self.pluginsController = ParamControllerTest.application.controller(
            PluginsController
        )

        self.currentController = ParamControllerTest.application.controller(
            CurrentController
        )

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

        self.currentBank = self.currentController.getCurrentBank()
        self.currentPatch = self.currentController.getCurrentPatch()

    def test_update_value(self):
        uri = 'http://guitarix.sourceforge.net/plugins/gx_reverb_stereo#_reverb_stereo'

        effectIndex = self.effectController.createEffect(
            self.currentBank,
            self.currentPatch,
            uri
        )

        plugin = self.pluginsController.plugins[uri]
        param = plugin['ports']['control']['output'][0]

        newValue = (param['maximum'] + param['minimum']) / 2
        self.controller.updateValue(
            self.currentBank,
            self.currentPatch,
            param,
            newValue
        )

        self.assertIsEqual(param['value'], newValue)

        self.controller.deleteEffect(
            self.currentBank,
            self.currentPatch,
            effectIndex
        )
