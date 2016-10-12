# -*- coding: utf-8 -*-
import unittest

from architecture.BankError import BankError
from architecture.privatemethod import privatemethod

from model.Bank import Bank
from model.Patch import Patch


class BankTest(unittest.TestCase):

    @privatemethod
    def generate_bank(self, name):
        return {
            "name": name,
            "patches": [{
                "name": "Decorator, a legend",
                "effects": [],
                "connections": []
            }, {
                "name": "Decorator 2, the otherside",
                "effects": [],
                "connections": []
            }]
        }

    def test_generate_bank(self):
        json = self.generate_bank('generic-bank')

        bank = Bank(json)

        self.assertEqual(json, bank.json)

    def test_generate_invalid_bank(self):
        json = self.generate_bank('generic-bank')
        del json["patches"]

        with self.assertRaises(BankError):
            Bank(json)

    def test_generate_invalid_bank_empty_patches(self):
        json = self.generate_bank('generic-bank')
        del json["patches"]
        json["patches"] = []

        with self.assertRaises(BankError):
            Bank(json)

    def test__get_item__(self):
        json = self.generate_bank('generic-bank')

        bank = Bank(json)
        self.assertTrue(json['patches'], bank['patches'])
        self.assertTrue(json['name'], bank['name'])

    def test__eq__(self):
        json = self.generate_bank('generic-bank')

        bank = Bank(json)
        bank2 = Bank(json)

        self.assertEqual(bank, bank2)

    def test__ne__(self):
        json = self.generate_bank('generic-bank')
        json2 = self.generate_bank('generic-bank-2')

        bank = Bank(json)
        bank2 = Bank(json2)

        self.assertNotEqual(bank, bank2)

    def test_json(self):
        json = self.generate_bank('generic-bank')

        bank = Bank(json)

        self.assertEqual(json, bank.json)

    def test_set_json(self):
        json = self.generate_bank('generic-bank')

        bank = Bank(json)

        json2 = self.generate_bank('generic-bank2')
        bank.json = json2

        self.assertNotEqual(json, bank.json)
        self.assertEqual(json2, bank.json)

    def test_undefined_index(self):
        json = self.generate_bank('generic-bank')

        bank = Bank(json)
        self.assertEqual(-1, bank.index)

    def test_set_index(self):
        json = self.generate_bank('generic-bank')

        bank = Bank(json)
        bank.index = 5.7

        self.assertEqual(5.7, bank.index)

    def test_add_patch(self):
        json = self.generate_bank('generic-bank')
        bank = Bank(json)

        patchJson = {
            'name': 'test-patch',
            'effects': [],
            'connections': []
        }
        patch = Patch(patchJson)

        bank.addPatch(patch)

        lastPatch = bank.patches[-1]
        self.assertEqual(lastPatch, patch)
        self.assertEqual(bank, patch.bank)

    def test_index_of_patch(self):
        json = self.generate_bank('generic-bank')
        bank = Bank(json)

        patchJson = {
            'name': 'test-patch',
            'effects': [],
            'connections': []
        }
        patch = Patch(patchJson)

        bank.addPatch(patch)

        index = 0
        for patch in bank.patches:
            self.assertEqual(index, patch.index)
            index += 1

    def test_swap(self):
        json = self.generate_bank('generic-bank')
        bank = Bank(json)

        patches = bank.patches

        bank.swapPatches(patches[0], patches[1])
        self.assertEqual(bank.patches, [patches[1], patches[0]])

    def test_wrong_swap(self):
        jsonA = self.generate_bank('generic-bank-a')
        jsonB = self.generate_bank('generic-bank-b')

        bankA = Bank(jsonA)
        bankB = Bank(jsonB)

        with self.assertRaises(BankError):
            bankA.swapPatches(bankA.patches[0], bankB.patches[1])
