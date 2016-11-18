from application.controller.current_controller import CurrentController
from application.controller.banks_controller import BanksController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch

from test.controller.controller_test import ControllerTest

from unittest.mock import MagicMock


class CurrentControllerTest(ControllerTest):
    application = None
    controller = None
    banks_controller = None

    def setUp(self):
        self.TOKEN = 'CURRENT_TOKEN'

        controller = CurrentControllerTest.application.controller
        self.controller = controller(CurrentController)
        self.banks_controller = controller(BanksController)
        self.notification_controller = controller(NotificationController)

        self.controller.set_patch = self.banks_controller.banks[0].patches[0]

    @property
    def bank_with_patch(self):
        bank = Bank('A bank')
        patch = Patch('A patch')
        bank.append(patch)

        return bank

    def test_current_patch(self):
        current_bank = self.controller.current_bank
        current_patch = self.controller.current_patch

        self.assertIsNotNone(current_patch)
        self.assertEqual(
            current_bank.patches[0],
            current_patch
        )

    def test_current_bank(self):
        current_bank = self.controller.current_bank

        self.assertIsNotNone(self.controller.current_bank)
        self.assertEqual(
            self.banks_controller.banks[0],
            current_bank
        )

    def test_is_current_bank(self):
        bank = self.bank_with_patch
        self.banks_controller.banks.append(bank)

        current_bank = self.controller.current_bank
        another_bank = self.banks_controller.banks[-1]

        self.assertTrue(self.controller.is_current_bank(current_bank))
        self.assertFalse(self.controller.is_current_bank(another_bank))

        self.banks_controller.banks.remove(bank)

    def test_is_current_patch(self):
        bank = self.bank_with_patch
        self.banks_controller.banks.append(bank)

        current_patch = self.controller.current_patch

        another_bank = self.banks_controller.banks[-1]
        another_patch = another_bank.patches[0]

        self.assertTrue(self.controller.is_current_patch(current_patch))
        self.assertFalse(self.controller.is_current_patch(another_patch))

        self.banks_controller.banks.remove(bank)

    def test_to_before_patch(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        patch = Patch('Other patch')
        self.controller.current_bank.append(patch)

        total_patches = len(self.controller.current_bank.patches)
        for id_patch in reversed(range(total_patches)):
            self.controller.to_before_patch()
            self.assertEqual(id_patch, self.controller.patch_number)
            observer.on_current_patch_changed.assert_called_with(self.controller.current_patch, None)

        for id_patch in reversed(range(total_patches)):
            self.controller.to_before_patch(self.TOKEN)
            self.assertEqual(id_patch, self.controller.patch_number)
            observer.on_current_patch_changed.assert_called_with(self.controller.current_patch, self.TOKEN)

        self.assertEqual(0, self.controller.patch_number)

        self.controller.current_bank.patches.remove(patch)

        self.notification_controller.unregister(observer)

    def test_to_next_patch(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        patch = Patch('Other patch')
        self.controller.current_bank.append(patch)

        total_patches = len(self.controller.current_bank.patches)
        for id_patch in reversed(range(total_patches)):
            self.controller.to_next_patch()
            self.assertEqual(id_patch, self.controller.patch_number)
            observer.on_current_patch_changed.assert_called_with(self.controller.current_patch, None)

        for id_patch in reversed(range(total_patches)):
            self.controller.to_next_patch(self.TOKEN)
            self.assertEqual(id_patch, self.controller.patch_number)
            observer.on_current_patch_changed.assert_called_with(self.controller.current_patch, self.TOKEN)

        self.assertEqual(0, self.controller.patch_number)

        self.controller.current_bank.patches.remove(patch)

        self.notification_controller.unregister(observer)

    def test_set_patch(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        patch = Patch('Other patch')
        self.controller.current_bank.append(patch)

        original_patch = self.controller.current_patch

        self.controller.set_patch(patch)
        self.assertEqual(patch.bank.patches.index(patch), self.controller.patch_number)
        observer.on_current_patch_changed.assert_called_with(patch, None)

        self.assertNotEqual(original_patch, self.controller.current_patch)
        self.assertEqual(patch, self.controller.current_patch)

        self.controller.set_patch(original_patch, self.TOKEN)
        self.assertEqual(0, self.controller.patch_number)
        observer.on_current_patch_changed.assert_called_with(original_patch, self.TOKEN)

        self.controller.current_bank.patches.remove(patch)

        self.notification_controller.unregister(observer)

    def test_set_patch_other_bank(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        bank = self.bank_with_patch
        self.banks_controller.banks.append(bank)

        original_patch = self.controller.current_patch

        self.controller.set_patch(bank.patches[0])
        self.assertEqual(0, self.controller.patch_number)
        self.assertEqual(self.banks_controller.banks.index(bank), self.controller.bank_number)
        observer.on_current_patch_changed.assert_called_with(bank.patches[0], None)

        self.assertNotEqual(original_patch, self.controller.current_patch)
        self.assertEqual(bank.patches[0], self.controller.current_patch)
        self.assertEqual(1, self.controller.bank_number)

        self.controller.set_patch(original_patch, self.TOKEN)
        self.assertEqual(0, self.controller.patch_number)
        self.assertEqual(0, self.controller.bank_number)
        observer.on_current_patch_changed.assert_called_with(original_patch, self.TOKEN)

        self.banks_controller.banks.remove(bank)
        self.notification_controller.unregister(observer)

    def test_set_patch_current_patch(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        self.controller.set_patch(self.controller.current_patch)
        observer.on_current_patch_changed.assert_not_called()

        self.notification_controller.unregister(observer)

"""
    def test_set_index_out_patch(self):
        with self.assertRaises(IndexError):
            self.controller.setPatch(5000)

    def test_before_bank(self):
        banks = self.banks_controller.banks.all
        for bank in reversed(banks):
            self.controller.toBeforeBank()
            self.assertEqual(bank, self.controller.currentBank)

    def test_next_bank(self):
        banks = self.banks_controller.banks.all
        for bank in banks:
            self.assertEqual(bank, self.controller.currentBank)
            self.controller.toNextBank()

        self.assertEqual(banks[0], self.controller.currentBank)

    def test_set_bank(self):
        firstBank = self.controller.currentBank

        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bank_number)

        self.assertNotEqual(firstBank, self.controller.currentBank)

    def test_setting_bank_patch_will_be_first(self):
        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bank_number)
        self.assertEqual(0, self.controller.patch_number)

    def test_set_index_out_bank(self):
        with self.assertRaises(IndexError):
            self.controller.setBank(5000)
"""
