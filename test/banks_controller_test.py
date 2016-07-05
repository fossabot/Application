# -*- coding: utf-8 -*-
import unittest

from architecture.BankError import BankError
from architecture.privatemethod import privatemethod

from Application import ApplicationSingleton

from controller.BanksController import BanksController
from controller.CurrentController import CurrentController


class BanksControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()

    def setUp(self):
        self.controller = self.get_controller(BanksController)
        self.currentController = self.get_controller(CurrentController)

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

    @privatemethod
    def get_controller(self, controller):
        return BanksControllerTest.application.controller(controller)

    @privatemethod
    def generate_bank(self, name):
        return {
            "name": name,
            "patches": [{
                "name": "Decorator, a legend",
                "effects": [],
                "connections": []
            }]
        }

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
        bank = self.generate_bank("test_create_bank")

        index = self.controller.createBank(bank)
        self.assertLess(totalBanks, len(self.controller.banks))

        self.controller.deleteBank(self.controller.banks[index])
        self.assertEqual(totalBanks, len(self.controller.banks))

    def test_update_bank(self):
        bankJson = self.generate_bank("test_update_bank")
        index = self.controller.createBank(bankJson)
        
        newName = 'Single a tom or chord?'

        bank = self.controller.banks[index]
        bankChangedJson = dict(bank.json)
        bankChangedJson['name'] = newName

        self.controller.updateBank(bank, bankChangedJson)

        changedName = bank['name']
        self.assertEqual(newName, changedName)

        self.controller.deleteBank(bank)

    def test_update_current_bank(self):
        currentBankData = dict(self.currentController.currentBank.json)

        originalName = currentBankData['name']
        newName = "test_update_current_bank"
        currentBankData['name'] = newName

        currentBank = self.currentController.currentBank

        self.controller.updateBank(currentBank, currentBankData)

        self.assertEqual(currentBank['name'], newName)

        currentBankData['name'] = originalName

        # Restoring name
        self.controller.updateBank(currentBank, currentBankData)

    def test_delete_bank(self):
        totalBanks = len(self.controller.banks)
        bank = self.generate_bank("test_delete_bank")

        # Added a bank
        index = self.controller.createBank(bank)
        self.assertLess(totalBanks, len(self.controller.banks))

        # Delete a bank
        self.controller.deleteBank(self.controller.banks[index])
        self.assertEqual(totalBanks, len(self.controller.banks))

    def test_delete_current_bank(self):
        bank = self.generate_bank("test_delete_current_bank")

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
