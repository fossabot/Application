from application.controller.patch_controller import PatchController
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
        self.notifier = controller(NotificationController)

    def test_create_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_patch - bank')
        patch = Patch('test_create_patch')
        patch2 = Patch('test_create_patch2')

        bank.append(patch)
        self.controller.create_patch(patch)
        observer.on_patch_updated.assert_called_with(patch, UpdateType.CREATED, None)

        bank.append(patch2)
        self.controller.create_patch(patch2, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch2, UpdateType.CREATED, self.TOKEN)

        self.controller.delete_patch(patch)
        self.controller.delete_patch(patch2)

        self.notifier.unregister(observer)

    def test_update_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_patch - bank')
        patch = Patch('test_update_patch')
        patch2 = Patch('test_update_patch2')
        patch3 = Patch('test_update_patch2')

        bank.append(patch)
        self.controller.create_patch(patch)

        bank.patches[bank.patches.index(patch)] = patch2
        self.controller.update_patch(patch2)

        observer.on_patch_updated.assert_called_with(patch2, UpdateType.UPDATED, None)

        bank.patches[bank.patches.index(patch2)] = patch3
        self.controller.update_patch(patch3, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch3, UpdateType.UPDATED, self.TOKEN)

        self.controller.delete_patch(patch3)
        self.notifier.unregister(observer)

    @unittest.skip("Not implemented")
    def test_update_current_patch(self):
        ...

    def test_delete_patch(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_delete_patch - bank')
        patch = Patch('test_delete_patch')
        patch2 = Patch('test_delete_patch2')

        bank.append(patch)
        bank.append(patch2)

        self.controller.create_patch(patch)
        self.controller.create_patch(patch2)

        self.controller.delete_patch(patch)
        observer.on_patch_updated.assert_called_with(patch, UpdateType.DELETED, None)
        self.controller.delete_patch(patch2, self.TOKEN)
        observer.on_patch_updated.assert_called_with(patch2, UpdateType.DELETED, self.TOKEN)

        self.notifier.unregister(observer)

    @unittest.skip("Not implemented")
    def test_update_deleted_patch(self):
        ...

    @unittest.skip("Not implemented")
    def test_delete_current_patch(self):
        ...

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
