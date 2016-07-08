# -*- coding: utf-8 -*-
import unittest

from architecture.privatemethod import privatemethod
from model.Bank import Bank
from model.Banks import Banks


class BanksTest(unittest.TestCase):

    @privatemethod
    def generate_bank(self, name, index=None):
        json = {
            "name": name,
            "patches": [{
                "name": "Decorator, a legend",
                "effects": [],
                "connections": []
            }]
        }

        if index is not None:
            json['index'] = index

        return Bank(json)

    def test_json(self):
        bank1 = self.generate_bank("Bank 1", 1)
        bank2 = self.generate_bank("Bank 2", 2)
        bank3 = self.generate_bank("Bank 3", 3)
        bank4 = self.generate_bank("Bank 4", 4)

        banks = Banks()
        banks.append(bank4)
        banks.append(bank3)
        banks.append(bank2)
        banks.append(bank1)

        banksJson = banks.json
        self.assertEqual(4, len(banksJson))

        banksJson.remove(bank1.json)
        banksJson.remove(bank2.json)
        banksJson.remove(bank3.json)
        banksJson.remove(bank4.json)

        self.assertEqual(0, len(banksJson))


    def test_json_banks_ordered(self):
        bank1 = self.generate_bank("Bank 1", 1)
        bank2 = self.generate_bank("Bank 2", 2)
        bank3 = self.generate_bank("Bank 3", 3)
        bank4 = self.generate_bank("Bank 4", 4)

        correctOrder = [bank1, bank2, bank3, bank4]

        banks = Banks()
        banks.append(bank4)
        banks.append(bank3)
        banks.append(bank2)
        banks.append(bank1)

        self.assertEqual(correctOrder, banks.all)

    def test__len__(self):
        bank1 = self.generate_bank("Bank 1", 1)
        bank2 = self.generate_bank("Bank 2", 2)
        bank3 = self.generate_bank("Bank 3", 3)
        bank4 = self.generate_bank("Bank 4", 4)

        banks = Banks()

        self.assertEqual(0, len(banks))
        banks.append(bank4)
        self.assertEqual(1, len(banks))
        banks.append(bank3)
        self.assertEqual(2, len(banks))
        banks.append(bank2)
        self.assertEqual(3, len(banks))
        banks.append(bank1)
        self.assertEqual(4, len(banks))

    def test__getitem__(self):
        bank1 = self.generate_bank("Bank 1", 1)
        bank2 = self.generate_bank("Bank 2", 2)
        bank3 = self.generate_bank("Bank 3", 3)
        bank4 = self.generate_bank("Bank 4", 4)

        banks = Banks()

        banks.append(bank1)
        banks.append(bank2)
        banks.append(bank3)
        banks.append(bank4)

        self.assertEqual(bank1, banks[1])
        self.assertEqual(bank2, banks[2])
        self.assertEqual(bank3, banks[3])
        self.assertEqual(bank4, banks[4])

        self.assertNotEqual(bank2, banks[1])

    def test__getitem__not_found(self):
        banks = Banks()
        banks.append(self.generate_bank("Bank 1", 1))

        with self.assertRaises(IndexError):
            banks[0]

    def test__delitem__(self):
        banks = Banks()
        banks.append(self.generate_bank("Bank 1", 1))

        del banks[1]

        self.assertEqual(0, len(banks))

    def test__getitem__not_found(self):
        banks = Banks()
        banks.append(self.generate_bank("Bank 1", 1))

        with self.assertRaises(IndexError):
            del banks[0]

    def test_append_bank(self):
        banks = Banks()

        self.assertEqual(0, len(banks))

        # no index implicit
        banks.append(self.generate_bank("Bank 1"))
        self.assertEqual(1, len(banks))

        # index specified
        banks.append(self.generate_bank("Bank 2", 1))
        self.assertEqual(2, len(banks))

        # no index specified explicit
        banks.append(self.generate_bank("Bank 3", -1))
        self.assertEqual(3, len(banks))
