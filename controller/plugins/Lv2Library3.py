# -*- coding: utf-8 -*-
from lib.lilvlib.plugins import get_all_plugins


class Lv2Library3(object):
    plugins = {}
    folders = ["/usr/lib/lv2/"]

    def __init__(self):
        for plugin in get_all_plugins():
            del plugin['errors']
            del plugin['warnings']
            self.plugins[plugin['uri']] = plugin

if __name__ == "__main__":
    lib = Lv2Library3()
    print(lib.plugins)