import json
import os


class Database(object):

    @staticmethod
    def read(url):
        with open(url) as data_file:
            return json.load(data_file)

    @staticmethod
    def save(url, data):
        json_file = open(url, "w+")
        json_file.write(json.dumps(data))
        json_file.close()

    @staticmethod
    def delete(url):
        os.remove(url)
