import json
import os
import asyncio


class Database(object):

    @staticmethod
    def read(url):
        with open(url) as data_file:
            return json.load(data_file)

    @staticmethod
    def save(url, data):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Database._save(url, data))

    @staticmethod
    @asyncio.coroutine
    def _save(url, data):
        json_file = open(url, "w+")
        json_file.write(json.dumps(data))
        json_file.close()

    @staticmethod
    def delete(url):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Database._delete(url))

    @staticmethod
    @asyncio.coroutine
    def _delete(url):
        os.remove(url)
