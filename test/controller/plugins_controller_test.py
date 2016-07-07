import unittest

from architecture.privatemethod import privatemethod

from Application import ApplicationSingleton
from controller.PluginsController import PluginsController, PluginTecnology
from controller.CurrentController import CurrentController


class PluginsControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()

    def setUp(self):
        self.controller = self.get_controller(PluginsController)
        currentController = self.get_controller(CurrentController)

        currentController.setBank(0)
        currentController.setPatch(0)

    @privatemethod
    def get_controller(self, controller):
        return PluginsControllerTest.application.controller(controller)

    def test_plugins_loaded(self):
        self.assertIsNot(0, len(self.controller.plugins))

    def test_get_plugin_by_techonology(self):
        self.assertIsInstance(
            self.controller.getBy(PluginTecnology.LV2),
            dict
        )
        self.assertIsInstance(
            self.controller.getBy(PluginTecnology.LADSPA),
            dict
        )
        self.assertIsInstance(
            self.controller.getBy(PluginTecnology.VST),
            dict
        )
