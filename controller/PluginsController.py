from util.Lv2Library import Lv2Library

from controller.Controller import Controller

class PluginsController(Controller):
    plugins = []

    def configure(self):
        self.plugins = Lv2Library().plugins