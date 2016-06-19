# -*- coding: utf-8 -*-
import unittest

from architecture.EffectException import EffectException
from architecture.privatemethod import privatemethod

from Application import ApplicationSingleton

from controller.EffectController import EffectController
from controller.PluginsController import PluginsController
from controller.CurrentController import CurrentController


class EffectControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()
        print("Loaded Application")

    def setUp(self):
        self.controller = EffectControllerTest.application.controller(
            EffectController
        )

        self.pluginsController = EffectControllerTest.application.controller(
            PluginsController
        )

        self.currentController = EffectControllerTest.application.controller(
            CurrentController
        )

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

        self.currentBank = self.currentController.getCurrentBank()
        self.currentPatch = self.currentController.getCurrentPatch()

    @privatemethod
    def total_effects_current_patch(self):
        return len(self.currentPatch['effects'])

    @privatemethod
    def any_plugin_uri(self):
        return list(self.pluginsController.plugins.keys())[0]

    def test_create_effect(self):
        totalEffects = self.total_effects_current_patch()
        effectIndex = self.controller.createEffect(
            self.currentBank,
            self.currentPatch,
            self.any_plugin_uri()
        )

        # Index is last effect + 1
        self.assertEqual(totalEffects, effectIndex)

        self.assertLess(totalEffects, self.total_effects_current_patch())

        self.controller.deleteEffect(
            self.currentBank,
            self.currentPatch,
            5000
        )

    def test_create_undefined_effect(self):
        with self.assertRaises(EffectException):
            self.controller.createEffect(
                self.currentBank,
                self.currentPatch,
                'http://undefined.plugin.uri'
            )

    def test_delete_effect(self):
        effectIndex = self.controller.createEffect(
            self.currentBank,
            self.currentPatch,
            self.any_plugin_uri()
        )
        totalEffects = self.total_effects_current_patch()

        self.controller.deleteEffect(
            self.currentBank,
            self.currentPatch,
            5000
        )
        self.controller.deletePatch(self.currentBank, effectIndex)

        self.assertEqual(totalEffects - 1, self.total_effects_current_patch())

    def test_delete_out_range_effect(self):
        with self.assertRaises(IndexError):
            self.controller.deleteEffect(
                self.currentBank,
                self.currentPatch,
                5000
            )
