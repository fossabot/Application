from controller.plugins.Lv2Library import Lv2Library
from controller.plugins.Lv2Library2 import Lv2Library2
from controller.plugins.LadspaLibrary import LadspaLibrary

from controller.Controller import Controller

class PluginsController(Controller):
    plugins = {}

    def configure(self):
        self.plugins = dict()
        #self.plugins.update(Lv2Library().plugins)
        self.plugins.update(Lv2Library2().plugins)
        self.plugins.update(LadspaLibrary().plugins)