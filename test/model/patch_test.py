# -*- coding: utf-8 -*-
import unittest

from architecture.privatemethod import privatemethod

from model.Patch import Patch
from model.Effect import Effect


class PatchTest(unittest.TestCase):

    @privatemethod
    def generate_patch(self, name):
        return {
            'name': name,
            'effects': [],
            'connections': []
        }

    def test_create_patch(self):
        json = self.generate_patch('generic-patch')

        patch = Patch(json)

        self.assertEqual(json, patch.json)

    def test_json(self):
        json = self.generate_patch('generic-patch')

        patch = Patch(json)

        self.assertEqual(json, patch.json)

    def test_set_json(self):
        """
        Show Patch.json (setter) for details of this test
        """
        json = self.generate_patch('generic-patch')
        json2 = self.generate_patch('generic-patch-2')

        patch = Patch(json)
        patch.json = json2

        self.assertEqual(json, patch.json)  # Show comment
        self.assertEqual(json2, patch.json)

    def test__getitem__(self):
        json = self.generate_patch('generic-patch')

        patch = Patch(json)

        self.assertEqual(patch.json['name'], patch['name'])

    def test__eq__(self):
        json = self.generate_patch('generic-patch')
        json2 = self.generate_patch('generic-patch')

        patch = Patch(json)
        patch2 = Patch(json2)

        self.assertEqual(patch, patch2)

    def test__ne__(self):
        json = self.generate_patch('generic-patch')
        json2 = self.generate_patch('generic-patch-2')

        patch = Patch(json)
        patch2 = Patch(json2)

        self.assertNotEqual(patch, patch2)

    def test_effects(self):
        json = self.generate_patch('generic-patch')
        json['effects'].append(self.generate_effect('Generic-EffectGxReverb-Stereo'))
        json['effects'].append(self.generate_effect('Generic-EffectGxReverb-Stereo2'))

        patch = Patch(json)

        effects = patch.effects
        for i in range(len(effects)):
            self.assertEqual(json['effects'][i], effects[i].json)

    def test_add_effect(self):
        json = self.generate_patch('generic-patch')

        patch = Patch(json)
        effect = Effect(self.generate_effect('Generic-EffectGxReverb-Stereo'))

        patch.addEffect(effect)

        self.assertEqual(effect, patch.effects[0])
        self.assertEqual(patch, effect.patch)

    def test_index_of_effect(self):
        json = self.generate_patch('generic-patch')

        patch = Patch(json)

        patch.addEffect(Effect(self.generate_effect('Generic-EffectGxReverb-Stereo1')))
        patch.addEffect(Effect(self.generate_effect('Generic-EffectGxReverb-Stereo2')))
        patch.addEffect(Effect(self.generate_effect('Generic-EffectGxReverb-Stereo3')))
        patch.addEffect(Effect(self.generate_effect('Generic-EffectGxReverb-Stereo4')))

        index = 0
        for effect in patch.effects:
            self.assertEqual(index, patch.indexOfEffect(effect))
            index += 1

    @privatemethod
    def generate_effect(self, name):
        return {
            "name": name,
            "uri": "http://generic.efx",
            "author": {},
            "label": "Generic-EffectGxReverb-Stereo",
            "status": True,
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
