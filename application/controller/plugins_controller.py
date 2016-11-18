from application.controller.controller import Controller

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

        '''
        self.plugins.update(Lv2Library().plugins)
        self.technology[PluginTechnology.LV2] = Lv2Library().plugins

        self.plugins.update(LadspaLibrary().plugins)
        self.technology[PluginTechnology.LADSPA] = LadspaLibrary().plugins
        '''

    def get_by(self, technology):
        """
        Get the plugins registred in PedalPi by technology

        :param PluginTechnology technology: PluginTechnology identifier
        """
        return self.technology[technology]
