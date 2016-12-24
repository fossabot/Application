from application.dao.database import Database


class CurrentDao(object):

    def __init__(self, data_path):
        self.data_path = data_path + 'current/'

    def load(self):
        return self._read_file()

    def save(self, bank_index, pedalboard_index):
        json = {
            "bank": bank_index,
            "pedalboard": pedalboard_index
        }

        Database.save(self._url(), json)

    def _read_file(self):
        return Database.read(self._url())

    def _url(self):
        return self.data_path + "current.json"
