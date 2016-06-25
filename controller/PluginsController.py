# -*- coding: utf-8 -*-

#from controller.plugins.Lv2Library import Lv2Library
from controller.plugins.Lv2LibraryMock import Lv2Library
from controller.plugins.LadspaLibrary import LadspaLibrary

from controller.Controller import Controller


from enum import Enum


class PluginTecnology(Enum):
    LV2 = 'lv2'
    LADSPA = 'ladspa'
    VST = 'vst'


class PluginsController(Controller):
    plugins = {}
    tecnology = {
        PluginTecnology.LV2: {},
        PluginTecnology.LADSPA: {},
        PluginTecnology.VST: {}
    }

    def configure(self):
        self.plugins = dict()
        
        self.plugins.update(Lv2Library().plugins)
        self.tecnology[PluginTecnology.LV2] = Lv2Library().plugins

        self.plugins.update(LadspaLibrary().plugins)
        self.tecnology[PluginTecnology.LADSPA] = LadspaLibrary().plugins

    def getBy(self, tecnology):
        '''
        @param tecnology PluginTecnology
        '''
        return self.tecnology[tecnology]
