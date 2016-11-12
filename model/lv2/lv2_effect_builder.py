import os

from dao.DataBank import DataBank
from model.lv2.lv2_plugin import Lv2Plugin
from model.lv2.lv2_effect import Lv2Effect


class Lv2EffectBuilder(object):

    def __init__(self):
        self.plugins = {}

        data = DataBank().read(os.path.dirname(__file__) + '/plugins.json')

        for plugin in data:
            self.plugins[plugin['uri']] = Lv2Plugin(plugin)

    @property
    def all(self):
        return self.plugins

    def build(self, lv2_uri):
        """
        Returns a new :class:`Lv2Effect` by the valid lv2_uri

        :param string lv2_uri:
        :return Lv2Effect: Effect created
        """
        return Lv2Effect(self.plugins[lv2_uri])
