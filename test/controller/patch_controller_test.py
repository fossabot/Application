from application.controller.current_controller import CurrentController
from application.controller.banks_controller import BanksController
from application.controller.patch_controller import PatchController, PatchError

from application.controller.notification_controller import NotificationController

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch
from pluginsmanager.model.update_type import UpdateType

import unittest
from unittest.mock import MagicMock


class PatchControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'PATCH_TOKEN'

        controller = PatchControllerTest.application.controller

        self.controller = controller(PatchController)
        self.current = controller(CurrentController)
        self.banks = controller(BanksController)
        self.notifier = controller(NotificationController)

    def test_create_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_patch - bank')
        patch = Patch('test_create_patch')
        patch2 = Patch('test_create_patch2')

        bank.append(patch)
        self.banks.create(bank)

        self.controller.created(patch)
        observer.on_patch_updated.assert_called_with(patch, UpdateType.CREATED, None, index=0, origin=bank)

        bank.append(patch2)
        self.controller.created(patch2, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch2, UpdateType.CREATED, self.TOKEN, index=1, origin=bank)

        self.controller.delete(patch)
        self.controller.delete(patch2)

        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_create_patch_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_patch_error - bank')
        patch = Patch('test_create_patch')
        bank.append(patch)

        with self.assertRaises(PatchError):
            self.controller.created(patch)

        observer.on_patch_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_update_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_patch - bank')
        patch = Patch('test_update_patch')

        self.banks.create(bank)

        bank.append(patch)
        self.controller.created(patch)

        patch.name = 'test_update_patch2'
        self.controller.update(patch)

        observer.on_patch_updated.assert_called_with(patch, UpdateType.UPDATED, None, index=0, origin=bank)

        patch.name = 'test_update_patch3'
        self.controller.update(patch, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch, UpdateType.UPDATED, self.TOKEN, index=0, origin=bank)

        self.controller.delete(patch)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_update_patch_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_current_patch - bank')
        patch = Patch('test_update_current_patch')
        bank.append(patch)

        with self.assertRaises(PatchError):
            self.controller.update(patch)

        observer.on_patch_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_update_current_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)
        original_patch = self.current.current_patch

        bank = Bank('test_update_current_patch - bank')
        patch = Patch('test_update_current_patch')

        self.banks.create(bank)

        bank.append(patch)
        self.controller.created(patch)

        self.current.set_patch(patch)

        patch.name = 'test_update_current_patch2'
        self.controller.update(patch)

        observer.on_patch_updated.assert_called_with(patch, UpdateType.UPDATED, None, index=0, origin=bank)

        self.assertEqual(self.current.current_patch, patch)
        self.assertEqual(self.current.current_bank, patch.bank)

        self.assertEqual(self.current.patch_number, patch.bank.patches.index(patch))
        self.assertEqual(self.current.bank_number, self.banks.banks.index(patch.bank))

        patch.name = 'test_update_current_patch3'
        self.controller.update(patch, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch, UpdateType.UPDATED, self.TOKEN, index=0, origin=bank)

        self.assertEqual(self.current.current_patch, patch)
        self.assertEqual(self.current.current_bank, patch.bank)

        self.assertEqual(self.current.patch_number, patch.bank.patches.index(patch))
        self.assertEqual(self.current.bank_number, self.banks.banks.index(patch.bank))

        self.current.set_patch(original_patch)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_replace(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_replace - bank')
        patch = Patch('test_replace')
        patch2 = Patch('test_replace2')
        patch3 = Patch('test_replace3')

        bank.append(patch)
        self.banks.create(bank)

        self.controller.replace(patch, patch2)
        observer.on_patch_updated.assert_called_with(patch2, UpdateType.UPDATED, None, index=0, origin=bank)

        self.controller.replace(patch2, patch3, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch3, UpdateType.UPDATED, self.TOKEN, index=0, origin=bank)

        self.controller.delete(patch3)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_replace_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_replace - bank')
        patch = Patch('test_replace')
        patch2 = Patch('test_replace2')

        bank.append(patch2)

        self.banks.create(bank)

        with self.assertRaises(PatchError):
            self.controller.replace(patch, patch2)

        observer.on_patch_updated.assert_not_called()

        bank.append(patch)

        with self.assertRaises(PatchError):
            self.controller.replace(patch, patch2)

        observer.on_patch_updated.assert_not_called()

        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_delete_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_delete_patch - bank')
        patch = Patch('test_delete_patch')
        patch2 = Patch('test_delete_patch2')

        self.banks.create(bank)

        bank.append(patch)
        bank.append(patch2)

        self.controller.created(patch)
        self.controller.created(patch2)

        self.controller.delete(patch)
        observer.on_patch_updated.assert_called_with(patch, UpdateType.DELETED, None, index=0, origin=bank)
        self.controller.delete(patch2, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch2, UpdateType.DELETED, self.TOKEN, index=0, origin=bank)

        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_delete_patch_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_delete_patch_error - bank')
        patch = Patch('test_delete_patch')

        bank.append(patch)
        with self.assertRaises(PatchError):
            self.controller.delete(patch)

        observer.on_patch_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_delete_current_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        original_patch = self.current.current_patch

        bank = Bank('test_delete_patch - bank')
        patch = Patch('test_delete_patch')
        patch2 = Patch('test_delete_patch2')

        self.banks.create(bank)

        bank.append(patch)
        bank.append(patch2)

        self.controller.created(patch)
        self.controller.created(patch2)

        self.current.set_patch(patch)
        self.controller.delete(patch)

        self.assertEqual(self.current.current_patch, patch2)
        self.assertEqual(self.current.current_bank, patch2.bank)

        self.assertEqual(self.current.patch_number, patch2.bank.patches.index(patch2))
        self.assertEqual(self.current.bank_number, self.banks.banks.index(patch2.bank))

        self.current.set_patch(original_patch)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    @unittest.skip("Not implemented")
    def test_swap(self):
        observer = MagicMock()
        self.notifier.register(observer)

        observer = MagicMock()
        self.notifier.register(observer)

        bank_a = Bank('test_swap - bank')
        patch_a = Patch('test_delete_patch 1')
        patch_a2 = Patch('test_delete_patch 2')

        bank_a.append(patch_a)
        bank_a.append(patch_a2)

        bank_b = Bank('test_swap - bank 2')
        patch_b = Patch('test_delete_patch 1')

        bank_b.append(patch_b)

        self.controller.swap(patch_a2, patch_b)

        self.assertEqual(bank_a.patches[1], patch_b)
        self.assertEqual(bank_b.patches[0], patch_a2)

        observer.on_patch_updated.assert_any_call(patch_b, UpdateType.UPDATED, None)
        observer.on_patch_updated.assert_any_call(patch_a2, UpdateType.UPDATED, None)

        self.controller.swap(patch_a2, patch_b, self.TOKEN)

        self.assertEqual(bank_a.patches[1], patch_a2)
        self.assertEqual(bank_b.patches[0], patch_b)

        observer.on_patch_updated.assert_any_call(patch_b, UpdateType.UPDATED, self.TOKEN)
        observer.on_patch_updated.assert_any_call(patch_a2, UpdateType.UPDATED, self.TOKEN)

        self.notifier.unregister(observer)

    @unittest.skip("Not implemented")
    def test_swap_current_patch(self):
        ...
