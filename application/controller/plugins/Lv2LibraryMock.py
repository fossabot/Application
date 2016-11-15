# -*- coding: utf-8 -*-
import os
from dao.DataBank import DataBank


class Lv2Library(object):
    plugins = {}

    def __init__(self):
        data = DataBank().read(os.path.dirname(__file__) + '/plugins.json')

        for plugin in data:
            self.plugins[plugin['uri']] = plugin
