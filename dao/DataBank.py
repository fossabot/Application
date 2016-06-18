# -*- coding: utf-8 -*-
import json
import os


class DataBank(object):

    @staticmethod
    def read(url):
        with open(url) as data_file:
            return json.load(data_file)

    @staticmethod
    def save(url, data):
        jsonFile = open(url, "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()

    @staticmethod
    def delete(url):
        os.remove(url)
