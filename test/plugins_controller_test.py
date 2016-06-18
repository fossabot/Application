import unittest

from Application import ApplicationSingleton


class PluginsControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()
        print("Loaded Application")

    def test_plugins_loaded(self):
        self.controller.plugins
        self.assertIsNot(0, len(self.controller.plugins))

    def test_get_plugin_by_techonology(self):
        self.assertIsInstance(
            self.controller.getBy(PluginTechology.LV2),
            list
        )
        self.assertIsInstance(
            self.controller.getBy(PluginTechology.LADSPA),
            list
        )
        self.assertIsInstance(
            self.controller.getBy(PluginTechology.VST),
            list
        )
