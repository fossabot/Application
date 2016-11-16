from application.controller.banks_controller import BanksController
from application.controller.notification_controller import NotificationController

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.update_type import UpdateType

import unittest
from unittest.mock import MagicMock


class BanksControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'BANKS_TOKEN'

        controller = BanksControllerTest.application.controller

        self.controller = controller(BanksController)
        self.notification_controller = controller(NotificationController)

    @unittest.skip("Not implemented")
    def test_load_banks(self):
        #self.assertIsNotNone(self.controller.banks)
        #self.assertNotEqual(0, len(self.controller.banks))
        ...

    def test_create_bank(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        bank = Bank('test_create_bank')
        index = self.controller.create_bank(bank)
        observer.on_bank_update.assert_called_with(bank, UpdateType.CREATED, None)
        self.assertEqual(index, self.controller.banks.index(bank))

        bank2 = Bank('test_create_bank_2')
        index2 = self.controller.create_bank(bank2, self.TOKEN)
        observer.on_bank_update.assert_called_with(bank2, UpdateType.CREATED, self.TOKEN)
        self.assertEqual(index2, self.controller.banks.index(bank2))

        self.notification_controller.unregister(observer)

        self.controller.delete_bank(bank)
        self.controller.delete_bank(bank2)

    def test_update_bank(self):
        observer = MagicMock()

        bank = Bank('test_update_bank')
        self.controller.create_bank(bank)

        self.notification_controller.register(observer)

        bank.name = 'test_update_bank_new'
        self.controller.update_bank(bank)
        observer.on_bank_update.assert_called_with(bank, UpdateType.UPDATED, None)

        bank.name = 'test_update_bank_new_new'
        self.controller.update_bank(bank, self.TOKEN)
        observer.on_bank_update.assert_called_with(bank, UpdateType.UPDATED, self.TOKEN)

        self.controller.delete_bank(bank)
        self.notification_controller.unregister(observer)

    @unittest.skip("Not implemented")
    def test_update_current_bank(self):
        ...

    def test_delete_bank(self):
        observer = MagicMock()

        total = len(self.controller.banks)

        bank = Bank('test_delete_bank')

        self.controller.create_bank(bank)

        self.notification_controller.register(observer)

        self.assertLess(total, len(self.controller.banks))
        self.controller.delete_bank(bank)
        self.assertEqual(total, len(self.controller.banks))

        observer.on_bank_update.assert_called_with(bank, UpdateType.DELETED, None)

        bank2 = Bank('test_delete_bank')
        self.controller.create_bank(bank2)
        self.controller.delete_bank(bank2, self.TOKEN)

        observer.on_bank_update.assert_called_with(bank2, UpdateType.DELETED, self.TOKEN)
        self.notification_controller.unregister(observer)

    @unittest.skip("Not implemented")
    def test_delete_current_bank(self):
        ...

    @unittest.skip("Not implemented")
    def test_swap(self):
        ...
