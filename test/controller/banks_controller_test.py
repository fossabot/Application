from controller.BanksController import BanksController
from controller.CurrentController import CurrentController
from controller.NotificationController import NotificationController

from model.UpdatesObserver import UpdateType

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank

import unittest
from unittest.mock import MagicMock


class BanksControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'BANKS_TOKEN'
        self.controller = self.get_controller(BanksController)
        self.currentController = self.get_controller(CurrentController)
        self.notificationController = self.get_controller(NotificationController)

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

    def get_controller(self, controller):
        return BanksControllerTest.application.controller(controller)

    @unittest.skip("Not implemented")
    def test_load_banks(self):
        #self.assertIsNotNone(self.controller.banks)
        #self.assertNotEqual(0, len(self.controller.banks))
        ...

    def test_create_bank(self):
        observer = MagicMock()
        self.notificationController.register(observer)

        bank = Bank('test_create_bank')
        index = self.controller.create_bank(bank)
        observer.onBankUpdate.assert_called_with(bank, UpdateType.CREATED, None)
        self.assertEqual(0, index)

        bank2 = Bank('test_create_bank_2')
        index2 = self.controller.create_bank(bank2, self.TOKEN)
        observer.onBankUpdate.assert_called_with(bank2, UpdateType.CREATED, self.TOKEN)
        self.assertEqual(1, index2)

        self.notificationController.unregister(observer)

        self.controller.delete_bank(bank)
        self.controller.delete_bank(bank2)

    def test_update_bank(self):
        observer = MagicMock()

        bank = Bank('test_update_bank')
        self.controller.create_bank(bank)

        self.notificationController.register(observer)

        bank.name = 'test_update_bank_new'
        self.controller.update_bank(bank)
        observer.onBankUpdate.assert_called_with(bank, UpdateType.UPDATED, None)

        bank.name = 'test_update_bank_new_new'
        self.controller.update_bank(bank, self.TOKEN)
        observer.onBankUpdate.assert_called_with(bank, UpdateType.UPDATED, self.TOKEN)

        self.controller.delete_bank(bank)

    @unittest.skip("Not implemented")
    def test_update_current_bank(self):
        ...

    def test_delete_bank(self):
        observer = MagicMock()

        total = len(self.controller.banks)

        bank = Bank('test_delete_bank')

        self.controller.create_bank(bank)

        self.notificationController.register(observer)

        self.assertLess(total, len(self.controller.banks))
        self.controller.delete_bank(bank)
        self.assertEqual(total, len(self.controller.banks))

        observer.onBankUpdate.assert_called_with(bank, UpdateType.DELETED, None)

        bank2 = Bank('test_delete_bank')
        self.controller.create_bank(bank2)
        self.controller.delete_bank(bank2, self.TOKEN)

        observer.onBankUpdate.assert_called_with(bank2, UpdateType.DELETED, self.TOKEN)

    @unittest.skip("Not implemented")
    def test_delete_current_bank(self):
        ...

    @unittest.skip("Not implemented")
    def test_swap(self):
        ...
