from controller.PluginsController import PluginsController, PluginTechnology
from controller.CurrentController import CurrentController

from test.controller.controller_test import ControllerTest


class PluginsControllerTest(ControllerTest):
    """
    Deprecated
    """

    def setUp(self):
        controller = PluginsControllerTest.application.controller
        self.controller = controller(PluginsController)
        current_controller = controller(CurrentController)

        current_controller.setBank(0)
        current_controller.setPatch(0)

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
