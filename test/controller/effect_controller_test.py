# -*- coding: utf-8 -*-
import unittest

from architecture.EffectException import EffectException
from architecture.privatemethod import privatemethod

from controller.EffectController import EffectController
from controller.PluginsController import PluginsController
from controller.CurrentController import CurrentController

from test.controller.controller_test import ControllerTest


class EffectControllerTest(ControllerTest):
    application = None
    controller = None

    def setUp(self):
        self.controller = self.get_controller(EffectController)
        self.pluginsController = self.get_controller(PluginsController)
        self.currentController = self.get_controller(CurrentController)

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

        self.currentBank = self.currentController.currentBank
        self.currentPatch = self.currentController.currentPatch

    @privatemethod
    def get_controller(self, controller):
        return EffectControllerTest.application.controller(controller)

    @privatemethod
    def total_effects_current_patch(self):
        return len(self.currentPatch['effects'])

    @privatemethod
    def any_plugin_uri(self):
        return list(self.pluginsController.plugins.keys())[0]

    @privatemethod
    def create_effect(self, uri=None):
        if uri is None:
            uri = self.any_plugin_uri()

        patch = self.currentPatch
        return self.controller.createEffect(patch, uri)

    def test_create_effect(self):
        totalEffects = self.total_effects_current_patch()

        effectIndex = self.create_effect()
        effect = self.currentPatch.effects[effectIndex]

        # Index is last effect + 1
        self.assertEqual(totalEffects, effectIndex)

        self.assertLess(totalEffects, self.total_effects_current_patch())

        self.controller.deleteEffect(effect)

    def test_create_undefined_effect(self):
        with self.assertRaises(EffectException):
            self.create_effect('http://undefined.plugin.uri')

    def test_delete_effect(self):
        effectIndex = self.create_effect()
        effect = self.currentPatch.effects[effectIndex]

        totalEffects = self.total_effects_current_patch()

        self.controller.deleteEffect(effect)

        self.assertEqual(totalEffects - 1, self.total_effects_current_patch())

    def test_delete_undefined_effect(self):
        #FIXME - Implement this
        pass
