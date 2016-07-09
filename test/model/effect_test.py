# -*- coding: utf-8 -*-
import unittest

from architecture.privatemethod import privatemethod
from model.Effect import Effect


class EffectTest(unittest.TestCase):
    @privatemethod
    def generate_effect(self, name, status=True):
        return {
            "name": name,
            "uri": "http://generic.efx",
            "author": {},
            "label": "Generic-EffectGxReverb-Stereo",
            "status": status,
            "ports": {
                "audio": {
                    "input": [],
                    "output": [{
                        "symbol": "out",
                        "name": "Out",
                        "scalePoints": [],
                        "units": {},
                        "ranges": {},
                        "properties": [],
                        "rangeSteps": None,
                        "designation": "",
                        "index": 5,
                        "shortName": "Out"
                    }]
                },
                "midi": {
                    "input": [],
                    "output": []
                },
                "control": {
                    "input": [{
                        "symbol": "dry_wet",
                        "name": "Dry/Wet",
                        "scalePoints": [],
                        "value": 50,
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
                    }],
                    "output": []
                }
            }
        }

    def test_generate_effect(self):
        json = self.generate_effect('generic-effect')

        effect = Effect(json)

        self.assertEqual(json, effect.json)

    def test_json(self):
        json = self.generate_effect('generic-effect')

        effect = Effect(json)

        self.assertEqual(json, effect.json)

    def test_set_json(self):
        """
        Show Effect.json (setter) for details of this test
        """
        json = self.generate_effect('generic-effect')
        json2 = self.generate_effect('generic-effect-2')

        effect = Effect(json)
        effect.json = json2

        self.assertEqual(json, effect.json)  # Show method comment
        self.assertEqual(json2, effect.json)

    def test__eq__(self):
        json = self.generate_effect('generic-effect')
        json2 = self.generate_effect('generic-effect')

        effect = Effect(json)
        effect2 = Effect(json2)

        self.assertEqual(effect, effect2)

    def test__ne__(self):
        json = self.generate_effect('generic-effect')
        json2 = self.generate_effect('generic-effect-2')

        effect = Effect(json)
        effect2 = Effect(json2)

        self.assertNotEqual(effect, effect2)

    def test__getitem__(self):
        json = self.generate_effect('generic-effect')

        effect = Effect(json)

        self.assertEqual(effect.json['name'], effect['name'])

    def test_params(self):
        json = self.generate_effect('generic-effect')
        paramsJson = json['ports']['control']['input']

        effect = Effect(json)

        params = effect.params
        for i in range(len(params)):
            self.assertEqual(paramsJson[i], params[i].json)

    def test_status(self):
        json = self.generate_effect('generic-effect', True)
        json2 = self.generate_effect('generic-effect', False)

        effect = Effect(json)
        effect2 = Effect(json2)

        self.assertEqual(True, effect.status)
        self.assertEqual(False, effect2.status)

    def test_get_index_of_param(self):
        json = self.generate_effect('generic-effect')

        effect = Effect(json)

        index = 0
        for param in effect.params:
            self.assertEqual(index, param.index)
            index += 1
