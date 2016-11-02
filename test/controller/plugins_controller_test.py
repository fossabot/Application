from architecture.privatemethod import privatemethod

from controller.PluginsController import PluginsController, PluginTechnology
from controller.CurrentController import CurrentController

from test.controller.controller_test import ControllerTest


class PluginsControllerTest(ControllerTest):
    controller = None

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
            self.controller.getBy(PluginTechnology.LV2),
            dict
        )
        self.assertIsInstance(
            self.controller.getBy(PluginTechnology.LADSPA),
            dict
        )
        self.assertIsInstance(
            self.controller.getBy(PluginTechnology.VST),
            dict
        )
