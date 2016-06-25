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

    def setUp(self):
        self.controller = BanksControllerTest.application.controller(
            BanksController
        )

        self.currentController = BanksControllerTest.application.controller(
            CurrentController
        )

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

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

        self.controller.deleteBank(self.controller.banks[index])
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

        index = self.controller.createBank(bank)
        
        newName = 'Single a tom or chord?'

        bankChanged = dict(self.controller.banks[index].json)
        bankChanged['name'] = newName

        self.controller.updateBank(self.controller.banks[index], bankChanged)

        changedName = self.controller.banks[index].data['name']
        self.assertEqual(newName, changedName)

        self.controller.deleteBank(self.controller.banks[index])

    def test_update_current_bank(self):
        currentBankData = dict(self.currentController.getCurrentBank().data)

        originalName = currentBankData['name']
        newName = "test_update_current_bank"
        currentBankData['name'] = newName

        self.controller.updateBank(
            self.currentController.getCurrentBank(),
            currentBankData
        )
        
        self.assertEqual(
            self.currentController.getCurrentBank().data['name'],
            newName
        )

        currentBankData['name'] = originalName

        # Restoring name
        self.controller.updateBank(
            self.currentController.getCurrentBank(),
            currentBankData
        )

    def test_delete_bank(self):
        totalBanks = len(self.controller.banks)
        bank = {
            "name": "test_delete_bank",
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
        self.controller.deleteBank(self.controller.banks[index])
        self.assertEqual(totalBanks, len(self.controller.banks))

    def test_delete_current_bank(self):
        bank = {
            "name": "test_delete_current_bank",
            "patches": [{
                "name": "Decorator, a legend",
                "effects": [],
                "connections": []
            }]
        }

        index = self.controller.createBank(bank)

        # Setted currend bank
        self.currentController.setBank(index)
        self.assertEqual(
            index,
            self.currentController.bankNumber
        )

        # Deleting bank
        totalBanks = len(self.controller.banks)

        self.controller.deleteBank(self.controller.banks[index])
        self.assertGreater(totalBanks, len(self.controller.banks))

        # Test updated current bank
        self.assertNotEqual(
            index,
            self.currentController.bankNumber
        )
