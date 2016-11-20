from application.controller.banks_controller import BanksController, BankError
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch
from pluginsmanager.model.update_type import UpdateType

import unittest
from unittest.mock import MagicMock


class BanksControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'BANKS_TOKEN'

        controller = BanksControllerTest.application.controller

        self.controller = controller(BanksController)
        self.current = controller(CurrentController)
        self.notifier = controller(NotificationController)

    def test_load_banks(self):
        self.assertIsNotNone(self.controller.banks)
        self.assertNotEqual(0, len(self.controller.banks))

    def test_create_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_bank')
        index = self.controller.create(bank)
        observer.on_bank_updated.assert_called_with(bank, UpdateType.CREATED, None)
        self.assertEqual(index, self.controller.banks.index(bank))

        bank2 = Bank('test_create_bank_2')
        index2 = self.controller.create(bank2, self.TOKEN)
        observer.on_bank_updated.assert_called_with(bank2, UpdateType.CREATED, self.TOKEN)
        self.assertEqual(index2, self.controller.banks.index(bank2))

        self.notifier.unregister(observer)

        self.controller.delete(bank)
        self.controller.delete(bank2)

    def test_create_created_bank(self):
        bank = Bank('test_create_created_bank')
        index = self.controller.create(bank)
        self.assertEqual(index, self.controller.banks.index(bank))

        observer = MagicMock()
        self.notifier.register(observer)

        with self.assertRaises(BankError):
            self.controller.create(bank, self.TOKEN)

        observer.on_bank_updated.assert_not_called()

        self.controller.delete(bank)

    def test_update_bank(self):
        observer = MagicMock()

        bank = Bank('test_update_bank')
        self.controller.create(bank)

        self.notifier.register(observer)

        bank.name = 'test_update_bank_new'
        self.controller.update(bank)
        observer.on_bank_updated.assert_called_with(bank, UpdateType.UPDATED, None)

        bank.name = 'test_update_bank_new_new'
        self.controller.update(bank, self.TOKEN)
        observer.on_bank_updated.assert_called_with(bank, UpdateType.UPDATED, self.TOKEN)

        self.controller.delete(bank)
        self.notifier.unregister(observer)

    def test_update_not_added_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_not_added_bank')
        with self.assertRaises(BankError):
            self.controller.update(bank)

        observer.on_bank_updated.assert_not_called()

    def test_update_current_bank(self):
        bank = Bank('test_update_current_bank 1')
        bank.append(Patch('test_update_current_bank patch'))

        original_current_patch = self.current.current_patch
        self.controller.create(bank)

        current_patch = bank.patches[0]
        self.current.set_patch(current_patch)

        del bank.patches[0]
        new_patch = Patch('test_update_current_bank patch2')
        bank.patches.append(new_patch)

        self.controller.update(bank)

        self.assertEqual(self.current.current_patch, new_patch)
        self.assertEqual(self.current.current_bank, new_patch.bank)

        self.assertEqual(self.current.patch_number, new_patch.bank.patches.index(new_patch))
        self.assertEqual(self.current.bank_number, self.controller.banks.index(new_patch.bank))

        self.current.set_patch(original_current_patch)

        self.controller.delete(bank)

    def test_replace_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_replace_bank 1')
        bank.append(Patch('test_replace_bank patch'))

        bank2 = Bank('test_replace_bank 2')
        bank2.append(Patch('test_replace_bank patch2'))

        bank3 = Bank('test_replace_bank 3')
        bank3.append(Patch('test_replace_bank patch3'))

        self.controller.create(bank)
        self.controller.replace(bank, bank2)
        observer.on_bank_updated.assert_any_call(bank2, UpdateType.UPDATED, None)

        self.controller.replace(bank2, bank3, self.TOKEN)
        observer.on_bank_updated.assert_any_call(bank3, UpdateType.UPDATED, self.TOKEN)

        self.controller.delete(bank3)
        self.notifier.unregister(observer)

    def test_replace_bank_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_replace_bank_error 1')
        bank.append(Patch('test_replace_bank_error patch'))

        bank2 = Bank('test_replace_bank_error 2')
        bank2.append(Patch('test_replace_bank_error patch2'))

        with self.assertRaises(BankError):
            self.controller.replace(bank, bank2)

        observer.on_bank_updated.assert_not_called()

        self.controller.create(bank)
        self.controller.create(bank2)

        observer.reset_mock()
        with self.assertRaises(BankError):
            self.controller.replace(bank, bank2)

        observer.on_bank_updated.assert_not_called()

        self.controller.delete(bank)
        self.controller.delete(bank2)
        self.notifier.unregister(observer)

    def test_replace_current_bank(self):
        bank = Bank('test_replace_current_bank 1')
        bank.append(Patch('test_replace_bank_error patch'))

        bank2 = Bank('test_replace_current_bank 2')
        bank2.append(Patch('test_replace_bank_error patch2'))

        original_current_patch = self.current.current_patch
        current_patch = bank.patches[0]

        self.controller.create(bank)
        self.current.set_patch(current_patch)

        self.controller.replace(bank, bank2)

        current_patch2 = bank2.patches[0]
        self.assertEqual(self.current.current_patch, current_patch2)
        self.assertEqual(self.current.current_bank, current_patch2.bank)

        self.assertEqual(self.current.patch_number, current_patch2.bank.patches.index(current_patch2))
        self.assertEqual(self.current.bank_number, self.controller.banks.index(current_patch2.bank))

        self.current.set_patch(original_current_patch)

        self.controller.delete(bank2)

    @unittest.skip('NOT IMPLEMENTED EMPTY CASES')
    def test_replace_current_empty_bank(self):
        bank = Bank('test_replace_current_bank 1')
        bank.append(Patch('test_replace_bank_error patch'))

        bank2 = Bank('test_replace_current_bank 2')

        current_patch = bank.patches[0]

        self.controller.create(bank)
        self.current.set_patch(current_patch)

        self.controller.replace(bank, bank2)

    def test_delete_bank(self):
        observer = MagicMock()

        total = len(self.controller.banks)

        bank = Bank('test_delete_bank')

        self.controller.create(bank)

        self.notifier.register(observer)

        self.assertLess(total, len(self.controller.banks))
        self.controller.delete(bank)
        self.assertEqual(total, len(self.controller.banks))

        observer.on_bank_updated.assert_called_with(bank, UpdateType.DELETED, None)

        bank2 = Bank('test_delete_bank')
        self.controller.create(bank2)
        self.controller.delete(bank2, self.TOKEN)

        observer.on_bank_updated.assert_called_with(bank2, UpdateType.DELETED, self.TOKEN)
        self.notifier.unregister(observer)

    def test_delete_current_bank(self):
        bank = Bank('test_delete_current_bank 1')
        bank.append(Patch('test_delete_current_bank patch'))

        bank2 = Bank('test_delete_current_bank 2')
        bank2.append(Patch('test_delete_current_bank patch'))

        original_current_patch = self.current.current_patch

        self.controller.create(bank)
        self.controller.create(bank2)

        current_patch = bank.patches[0]
        self.current.set_patch(current_patch)

        self.assertEqual(self.current.current_patch, current_patch)
        self.assertEqual(self.current.current_bank, current_patch.bank)

        self.assertEqual(self.current.patch_number, current_patch.bank.patches.index(current_patch))
        self.assertEqual(self.current.bank_number, self.controller.banks.index(current_patch.bank))

        self.controller.delete(bank, bank2)

        current_patch2 = bank2.patches[0]

        self.assertEqual(self.current.current_bank, current_patch2.bank)
        self.assertEqual(self.current.current_patch, current_patch2)

        self.assertEqual(self.current.patch_number, current_patch2.bank.patches.index(current_patch2))
        self.assertEqual(self.current.bank_number, self.controller.banks.index(current_patch2.bank))

        self.current.set_patch(original_current_patch)
        self.controller.delete(bank2)

    def test_delete_current_bank_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_replace_bank_error 1')
        bank.append(Patch('test_replace_bank_error patch'))

        with self.assertRaises(BankError):
            self.controller.delete(bank)

        observer.on_bank_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_swap(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_swap 1')
        bank2 = Bank('test_swap 2')

        index = self.controller.create(bank)
        index2 = self.controller.create(bank2)

        self.assertEqual(bank, self.controller.banks[index])
        self.assertEqual(bank2, self.controller.banks[index2])

        self.controller.swap(bank, bank2)
        observer.on_bank_updated.assert_any_call(bank, UpdateType.UPDATED, None)
        observer.on_bank_updated.assert_any_call(bank2, UpdateType.UPDATED, None)

        self.assertEqual(bank, self.controller.banks[index2])
        self.assertEqual(bank2, self.controller.banks[index])

        self.controller.swap(bank, bank2, self.TOKEN)
        observer.on_bank_updated.assert_any_call(bank, UpdateType.UPDATED, self.TOKEN)
        observer.on_bank_updated.assert_any_call(bank2, UpdateType.UPDATED, self.TOKEN)

        self.assertEqual(bank, self.controller.banks[index])
        self.assertEqual(bank2, self.controller.banks[index2])

        self.notifier.unregister(observer)

        self.controller.delete(bank)
        self.controller.delete(bank2)

    def test_swap_error(self):
        bank = Bank('test_swap_error 1')
        bank2 = Bank('test_swap_error 2')

        self.controller.create(bank)

        observer = MagicMock()
        self.notifier.register(observer)

        with self.assertRaises(BankError):
            self.controller.swap(bank, bank2)

        with self.assertRaises(BankError):
            self.controller.swap(bank2, bank)

        observer.on_bank_updated.assert_not_called()

        self.controller.delete(bank)

    def test_swap_current_bank(self):
        bank = Bank('test_swap_current_bank 1')
        bank.append(Patch('test_swap_current_bank patch'))

        bank2 = Bank('test_swap_current_bank 2')
        bank2.append(Patch('test_swap_current_bank patch2'))

        original_current_patch = self.current.current_patch

        self.controller.create(bank)
        self.controller.create(bank2)

        current_patch = bank.patches[0]
        self.current.set_patch(current_patch)

        self.assertEqual(self.current.current_patch, current_patch)
        self.assertEqual(self.current.current_bank, current_patch.bank)

        self.assertEqual(self.current.patch_number, current_patch.bank.patches.index(current_patch))
        self.assertEqual(self.current.bank_number, self.controller.banks.index(current_patch.bank))

        self.controller.swap(bank, bank2)

        self.assertEqual(self.current.current_patch, current_patch)
        self.assertEqual(self.current.current_bank, current_patch.bank)

        self.assertEqual(self.current.patch_number, current_patch.bank.patches.index(current_patch))
        self.assertEqual(self.current.bank_number, self.controller.banks.index(current_patch.bank))

        self.controller.swap(bank2, bank)

        self.assertEqual(self.current.current_patch, current_patch)
        self.assertEqual(self.current.current_bank, current_patch.bank)

        self.assertEqual(self.current.patch_number, current_patch.bank.patches.index(current_patch))
        self.assertEqual(self.current.bank_number, self.controller.banks.index(current_patch.bank))

        self.current.set_patch(original_current_patch)

        self.controller.delete(bank)
        self.controller.delete(bank2)
