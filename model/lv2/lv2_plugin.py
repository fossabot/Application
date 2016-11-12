
class Lv2Plugin(object):

    def __init__(self, json):
        self._json = json

    def __getitem__(self, key):
        """
        :param string key: Property key
        :return: Returns a Plugin property
        """
        return self._json[key]
