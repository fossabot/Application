import unittest

class PluginsControllerTest(unittest.TestCase):
    application = None
    controller = None

        
    def testPluginsLoaded(self):
        self.controller.plugins
        self.assertIsNot(0, len(self.controller.plugins))
        
    def testGetPluginsByTechonology(self):
        self.assertIsInstance(self.controller.getBy(PluginTechology.LV2), list)
        self.assertIsInstance(self.controller.getBy(PluginTechology.LADSPA), list)
        self.assertIsInstance(self.controller.getBy(PluginTechology.VST), list)
