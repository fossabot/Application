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

        self.currentBank = self.currentController.currentBank
        self.currentPatch = self.currentController.currentPatch

    def test_update_value(self):
        uri = 'http://guitarix.sourceforge.net/plugins/gx_reverb_stereo#_reverb_stereo'

        effectIndex = self.effectController.createEffect(
            self.currentBank,
            self.currentPatch,
            uri
        )

        effect = self.currentPatch['effects'][effectIndex]
        param = effect['ports']['control']['input'][0]

        ranges = param['ranges']
        newValue = (ranges['maximum'] + ranges['minimum']) / 2
        self.controller.updateValue(
            self.currentBank,
            self.currentPatch,
            param,
            newValue
        )

        self.assertEqual(param['value'], newValue)

        self.effectController.deleteEffect(
            self.currentBank,
            self.currentPatch,
            effectIndex
        )
