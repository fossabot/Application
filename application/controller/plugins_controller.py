from application.controller.controller import Controller

from enum import Enum

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


class PluginTechnology(Enum):
    """
    Enumeration for informs audio plugins technology
    """
    LV2 = 'lv2'
    LADSPA = 'ladspa'
    VST = 'vst'


class PluginsController(Controller):

    def __init__(self, application):
        super(PluginsController, self).__init__(application)
        self.lv2_builder = None

    def configure(self):
        self.lv2_builder = Lv2EffectBuilder()

    def by(self, technology):
        """
        Get the plugins registered in PedalPi by technology

        :param PluginTechnology technology: PluginTechnology identifier
        """
        if technology == PluginTechnology.LV2 \
        or str(technology).upper() == PluginTechnology.LV2.value.upper():
            return self.lv2_builder.all
        else:
            return []

    def lv2_effect(self, lv2_uri):
        return self.lv2_builder.build(lv2_uri)
