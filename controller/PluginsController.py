# -*- coding: utf-8 -*-

#from controller.plugins.Lv2Library import Lv2Library
from controller.plugins.Lv2LibraryMock import Lv2Library
from controller.plugins.LadspaLibrary import LadspaLibrary

from controller.Controller import Controller


from enum import Enum


class PluginTechnology(Enum):
    """
    Enumeration for informs audio plugins technology
    """
    LV2 = 'lv2'
    LADSPA = 'ladspa'
    VST = 'vst'


class PluginsController(Controller):
    plugins = {}
    
    technology = {
        PluginTechnology.LV2: {},
        PluginTechnology.LADSPA: {},
        PluginTechnology.VST: {}
    }

    def configure(self):
        self.plugins = dict()

        self.plugins.update(Lv2Library().plugins)
        self.technology[PluginTechnology.LV2] = Lv2Library().plugins

        self.plugins.update(LadspaLibrary().plugins)
        self.technology[PluginTechnology.LADSPA] = LadspaLibrary().plugins

    def getBy(self, technology):
        """
        Get the plugins registred in PedalPi by technology

        :param PluginTechnology technology: PluginTechnology identifier
        """
        return self.technology[technology]
