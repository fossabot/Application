# -*- coding: utf-8 -*-
import unittest

from Application import ApplicationSingleton

from controller.BanksController import BanksController
from controller.CurrentController import CurrentController

from architecture.BankError import BankError


class BanksControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()
        print("Loaded Application")

    def setUp(self):
        self.controller = BanksControllerTest.application.controller(
            BanksController
        )

        currentController = BanksControllerTest.application.controller(
            CurrentController
        )

        currentController.setBank(0)
        currentController.setPatch(0)

    def test_load_banks(self):
        self.assertIsNotNone(self.controller.banks)
        self.assertNotEqual(0, len(self.controller.banks))

    def test_create_bank_empty_patch(self):
        totalBanks = len(self.controller.banks)
        bank = {
            "name": "test_create_bank_empty_patch",
            "patches": []
        }

        with self.assertRaises(BankError):
            self.controller.createBank(bank)

        # Bank not added
        self.assertEqual(totalBanks, len(self.controller.banks))

    def test_create_bank(self):
        totalBanks = len(self.controller.banks)
        bank = {
            "name": "test_create_bank",
            "patches": [{
                "name": "Decorator, a legend",
                "effects": [],
                "connections": []
            }]
        }

        index = self.controller.createBank(bank)
        self.assertLess(totalBanks, len(self.controller.banks))

        del self.controller.banks[index]
        self.assertEqual(totalBanks, len(self.controller.banks))

    def test_update_bank(self):
        bank = {
            "name": "test_update_bank",
            "patches": [{
                "name": "Decorator, a legend",
                "effects": [],
                "connections": []
            }]
        }

        newName = 'Single a tom or chord?'

        bankChanged = dict()
        bankChanged.update(bank)
        bankChanged['name'] = newName

        index = self.controller.createBank(bank)
        self.controller.updateBank(self.controller.banks[index], bankChanged)

        changedName = self.controller.banks[index].data['name']
        self.assertEqual(newName, changedName)

        del self.controller.banks[index]

    def test_delete_bank(self):
        totalBanks = len(self.controller.banks)
        bank = {
            "name": "test_create_bank",
            "patches": [{
                "name": "Decorator, a legend",
                "effects": [],
                "connections": []
            }]
        }

        # Added a bank
        index = self.controller.createBank(bank)
        self.assertLess(totalBanks, len(self.controller.banks))

        # Delete a bank
        del self.controller.banks[index]
        self.assertEqual(totalBanks, len(self.controller.banks))
