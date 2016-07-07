# -*- coding: utf-8 -*-
import unittest

from architecture.privatemethod import privatemethod
from model.Param import Param


class ParamTest(unittest.TestCase):

    @privatemethod
    def generate_param(self, name, value=50):
        return {
            "symbol": "dry_wet",
            "name": name,
            "scalePoints": [],
            "value": value,
            "units": {},
            "ranges": {
                "minimum": 0,
                "maximum": 100,
                "default": 50
            },
            "properties": [],
            "rangeSteps": None,
            "designation": "",
            "index": 0,
            "shortName": "Dry/Wet"
        }

    def test_generate_param(self):
        json = self.generate_param('generic-param')

        param = Param(json)

        self.assertEqual(json, param.json)

    def test_json(self):
        json = self.generate_param('generic-param')

        param = Param(json)

        self.assertEqual(json, param.json)

    def test__eq__(self):
        json = self.generate_param('generic-param')
        json2 = self.generate_param('generic-param')

        param = Param(json)
        param2 = Param(json2)

        self.assertEqual(param, param)

    def test__ne__(self):
        json = self.generate_param('generic-param')
        json2 = self.generate_param('generic-param-2')

        param = Param(json)
        param2 = Param(json2)

        self.assertNotEqual(param, param2)

    def test__getitem__(self):
        json = self.generate_param('generic-param')

        param = Param(json)

        self.assertEqual(param.json['name'], param['name'])
        self.assertEqual(param.json['value'], param['value'])

    def test_value(self):
        json = self.generate_param('generic-param', 55)

        param = Param(json)

        self.assertEqual(param.json['value'], param.value)

    def test_set_value(self):
        json = self.generate_param('generic-param', 55)

        param = Param(json)
        param.value = 10

        self.assertNotEqual(55, param.value)
        self.assertEqual(10, param.value)
