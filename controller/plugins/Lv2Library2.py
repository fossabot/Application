from os import listdir
from os.path import isfile, join

from .rdfmodel.lv2 import Bundle


class Lv2Library2:
    plugins = {}
    folders = ["/usr/lib/lv2/"]

    def __init__(self):
        folders = []
        for lv2Folder in self.folders:
            folders += [join(lv2Folder, f) for f in listdir(lv2Folder) if not isfile(join(lv2Folder, f))]

        for folder in folders:
            try:
                self.plugins.update(self.getPlugins(folder))

            except Exception as e:
                #import traceback
                #traceback.print_exc()
                print(e)
                print("[ERROR] Lv2 file error:", folder)

    def getPlugins(self, folder):
        plugins = {}
        bundle = Bundle(folder)
        for lv2Plugin in bundle.data['plugins']:
            plugins[lv2Plugin['url']] = lv2Plugin

        return plugins

if __name__ == "__main__":
    lib = Lv2Library2()
    print(lib.plugins)