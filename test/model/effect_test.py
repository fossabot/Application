# -*- coding: utf-8 -*-
import unittest

from model.Effect import Effect
from model.Patch import Patch


class EffectTest(unittest.TestCase):
    def _generate_effect(self, name, status=True):
        return {
            "name": name,
            "uri": "http://generic.efx",
            "author": {},
            "label": "Generic-EffectGxReverb-Stereo",
            "status": status,
            "ports": {
                "audio": {
                    "input": [{
                        "ranges": {},
                        "designation": "",
                        "index": 4,
                        "units": {},
                        "shortName": "in",
                        "properties": [],
                        "name": "in",
                        "symbol": "in",
                        "rangeSteps": None,
                        "scalePoints": []
                    }, {
                        "ranges": {},
                        "designation": "",
                        "index": 4,
                        "units": {},
                        "shortName": "in-right",
                        "properties": [],
                        "name": "in",
                        "symbol": "in-right",
                        "rangeSteps": None,
                        "scalePoints": []
                    }],
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

    def _generate_patch_json(self, name='generic-patch'):
        return {
            'name': name,
            'effects': [],
            'connections': []
        }

    def test_generate_effect(self):
        json = self._generate_effect('generic-effect')

        effect = Effect(json)

        self.assertEqual(json, effect.json)

    def test_json(self):
        json = self._generate_effect('generic-effect')

        effect = Effect(json)

        self.assertEqual(json, effect.json)

    def test_set_json(self):
        """
        Show Effect.json (setter) for details of this test
        """
        json = self._generate_effect('generic-effect')
        json2 = self._generate_effect('generic-effect-2')

        effect = Effect(json)
        effect.json = json2

        self.assertEqual(json, effect.json)  # Show method comment
        self.assertEqual(json2, effect.json)

    def test__eq__(self):
        json = self._generate_effect('generic-effect')
        json2 = self._generate_effect('generic-effect')

        effect = Effect(json)
        effect2 = Effect(json2)

        self.assertEqual(effect, effect2)

    def test__ne__(self):
        json = self._generate_effect('generic-effect')
        json2 = self._generate_effect('generic-effect-2')

        effect = Effect(json)
        effect2 = Effect(json2)

        self.assertNotEqual(effect, effect2)

    def test__getitem__(self):
        json = self._generate_effect('generic-effect')

        effect = Effect(json)

        self.assertEqual(effect.json['name'], effect['name'])

    def test_params(self):
        json = self._generate_effect('generic-effect')
        params_json = json['ports']['control']['input']

        effect = Effect(json)

        params = effect.params
        for i in range(len(params)):
            self.assertEqual(params_json[i], params[i].json)

    def test_status(self):
        json = self._generate_effect('generic-effect', True)
        json2 = self._generate_effect('generic-effect', False)

        effect = Effect(json)
        effect2 = Effect(json2)

        self.assertEqual(True, effect.status)
        self.assertEqual(False, effect2.status)

    def test_get_index_of_param(self):
        json = self._generate_effect('generic-effect')

        effect = Effect(json)

        index = 0
        for param in effect.params:
            self.assertEqual(index, param.index)
            index += 1

    def test_index(self):
        patch_json = self._generate_patch_json()
        patch = Patch(patch_json)

        json = self._generate_effect('generic-effect')
        effect = Effect(json)

        json = self._generate_effect('generic-effect-2')
        effect2 = Effect(json)

        patch.addEffect(effect)
        patch.addEffect(effect2)

        self.assertEqual(effect.index, 0)
        self.assertEqual(effect2.index, 1)

    def test_representation(self):
        patch_json = self._generate_patch_json()
        patch = Patch(patch_json)

        json = self._generate_effect('generic-effect')
        effect = Effect(json)

        json2 = self._generate_effect('generic-effect-2')
        effect2 = Effect(json2)

        patch.addEffect(effect)
        patch.addEffect(effect2)

        self.assertEqual(effect.representation, 'effect_0')
        self.assertEqual(effect2.representation, 'effect_1')

    def test_inputs(self):
        json = self._generate_effect('generic-effect')
        inputs = json['ports']['audio']['input']

        effect = Effect(json)
        self.assertEqual(effect.inputs, inputs)

    def test_outputs(self):
        json = self._generate_effect('generic-effect')
        outputs = json['ports']['audio']['output']

        effect = Effect(json)
        self.assertEqual(effect.outputs, outputs)

    def test_connections(self):
        patch_json = self._generate_patch_json()
        patch = Patch(patch_json)

        json = self._generate_effect('generic-effect')
        effect = Effect(json)

        json2 = self._generate_effect('generic-effect-2')
        effect2 = Effect(json2)

        json3 = self._generate_effect('generic-effect-3')
        effect3 = Effect(json3)

        json4 = self._generate_effect('generic-effect-4')
        effect4 = Effect(json4)

        patch.addEffect(effect)
        patch.addEffect(effect2)
        patch.addEffect(effect3)
        patch.addEffect(effect4)

        patch.connect(effect, effect.outputs[0], effect2, effect2.inputs[0])
        patch.connect(effect, effect.outputs[0], effect2, effect3.inputs[1])
        patch.connect(effect2, effect2.outputs[0], effect2, effect3.inputs[1])
        patch.connect(effect4, effect4.outputs[0], effect, effect.inputs[1])

        effect_connections = [
            {'out': 'effect_0:out', 'in': 'effect_1:in'},
            {'out': 'effect_0:out', 'in': 'effect_1:in-right'},
            {'out': 'effect_3:out', 'in': 'effect_0:in-right'}
        ]

        self.assertEqual(effect_connections, list(effect.connections))
