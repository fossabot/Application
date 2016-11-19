from application.controller.current_controller import CurrentController
from application.controller.banks_controller import BanksController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch

from test.controller.controller_test import ControllerTest

from unittest.mock import MagicMock


class CurrentControllerTest(ControllerTest):
    def setUp(self):
        self.TOKEN = 'CURRENT_TOKEN'

        controller = CurrentControllerTest.application.controller
        self.controller = controller(CurrentController)
        self.banks_controller = controller(BanksController)
        self.notifier = controller(NotificationController)

        self.controller.set_patch(self.banks_controller.banks[0].patches[0])

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
        self.banks_controller.create_bank(bank)

        current_bank = self.controller.current_bank
        another_bank = self.banks_controller.banks[-1]

        self.assertTrue(self.controller.is_current_bank(current_bank))
        self.assertFalse(self.controller.is_current_bank(another_bank))

        self.banks_controller.delete_bank(bank)

    def test_is_current_patch(self):
        bank = self.bank_with_patch
        self.banks_controller.create_bank(bank)

        current_patch = self.controller.current_patch

        another_bank = self.banks_controller.banks[-1]
        another_patch = another_bank.patches[0]

        self.assertTrue(self.controller.is_current_patch(current_patch))
        self.assertFalse(self.controller.is_current_patch(another_patch))

        self.banks_controller.delete_bank(bank)

    def test_to_before_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

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

        self.notifier.unregister(observer)

    def test_to_next_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        patch = Patch('Other patch')
        self.controller.current_bank.append(patch)

        total_patches = len(self.controller.current_bank.patches)
        patch_initial_index = self.controller.patch_number
        for id_patch in range(total_patches):
            self.assertEqual(id_patch + patch_initial_index, self.controller.patch_number)
            self.controller.to_next_patch()
            observer.on_current_patch_changed.assert_called_with(self.controller.current_patch, None)

        for id_patch in range(total_patches):
            self.assertEqual(id_patch, self.controller.patch_number)
            self.controller.to_next_patch(self.TOKEN)
            observer.on_current_patch_changed.assert_called_with(self.controller.current_patch, self.TOKEN)

        self.assertEqual(0, self.controller.patch_number)

        self.controller.current_bank.patches.remove(patch)

        self.notifier.unregister(observer)

    def test_set_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

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

        self.notifier.unregister(observer)

    def test_set_patch_other_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_patch
        self.banks_controller.create_bank(bank)

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

        self.banks_controller.delete_bank(bank)
        self.notifier.unregister(observer)

    def test_set_patch_current_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        self.controller.set_patch(self.controller.current_patch)
        observer.on_current_patch_changed.assert_not_called()

        self.notifier.unregister(observer)

    def test_set_patch_not_added(self):
        bank = self.bank_with_patch
        with self.assertRaises(ValueError):
            self.controller.set_patch(bank.patches[0])

    def test_before_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_patch
        self.banks_controller.create_bank(bank)

        for b in reversed(self.banks_controller.banks):
            self.controller.to_before_bank()
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_patch_changed.assert_called_with(b.patches[0], None)

        for b in reversed(self.banks_controller.banks):
            self.controller.to_before_bank(self.TOKEN)
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_patch_changed.assert_called_with(b.patches[0], self.TOKEN)

        self.banks_controller.delete_bank(bank)
        self.notifier.unregister(observer)

    def test_next_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_patch
        self.banks_controller.create_bank(bank)

        self.controller.to_before_bank()
        for b in self.banks_controller.banks:
            self.controller.to_next_bank()
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_patch_changed.assert_called_with(b.patches[0], None)

        for b in self.banks_controller.banks:
            self.controller.to_next_bank(self.TOKEN)
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_patch_changed.assert_called_with(b.patches[0], self.TOKEN)

        self.controller.to_next_bank()

        self.banks_controller.delete_bank(bank)
        self.notifier.unregister(observer)

    def test_set_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_patch
        index = self.banks_controller.create_bank(bank)

        first_bank = self.controller.current_bank

        self.controller.set_bank(bank)
        self.assertEqual(index, self.controller.bank_number)
        self.assertNotEqual(first_bank, self.controller.current_bank)
        observer.on_current_patch_changed.assert_called_with(bank.patches[0], None)

        # Patch will be the first
        self.assertEqual(index, self.controller.bank_number)
        self.assertEqual(0, self.controller.patch_number)

        self.controller.set_bank(first_bank, self.TOKEN)
        observer.on_current_patch_changed.assert_called_with(first_bank.patches[0], self.TOKEN)

        self.banks_controller.delete_bank(bank)
        self.notifier.unregister(observer)

    def test_set_bank_not_added(self):
        bank = self.bank_with_patch
        with self.assertRaises(ValueError):
            self.controller.set_bank(bank)

    def test_set_bank_current_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        self.controller.set_bank(self.controller.current_bank)
        observer.on_current_patch_changed.assert_not_called()

        self.notifier.unregister(observer)
