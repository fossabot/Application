# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
