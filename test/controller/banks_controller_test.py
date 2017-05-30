# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from application.controller.banks_controller import BanksController, BankError
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.update_type import UpdateType

from unittest.mock import MagicMock


class BanksControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'BANKS_TOKEN'

        controller = BanksControllerTest.application.controller

        self.controller = controller(BanksController)
        self.current = controller(CurrentController)
        self.notifier = controller(NotificationController)

        self.manager = self.controller.manager

    def test_load_banks(self):
        self.assertIsNotNone(self.controller.banks)
        self.assertNotEqual(0, len(self.controller.banks))

    def test_created_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_created_bank')
        self.manager.append(bank)
        self.controller.created(bank)
        observer.on_bank_updated.assert_called_with(bank, UpdateType.CREATED, index=bank.index, origin=self.manager, token=None)

        bank2 = Bank('test_created_bank_2')
        self.manager.append(bank2)
        self.controller.created(bank2, self.TOKEN)
        observer.on_bank_updated.assert_called_with(bank2, UpdateType.CREATED, index=bank2.index, origin=self.manager, token=self.TOKEN)

        self.notifier.unregister(observer)

        self.manager.banks.remove(bank)
        self.manager.banks.remove(bank2)

    def test_created_bank_not_added_manager(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_created_bank')
        with self.assertRaises(BankError):
            self.controller.created(bank, self.TOKEN)

        observer.on_bank_updated.assert_not_called()
        self.notifier.unregister(observer)

    def test_updated_bank(self):
        observer = MagicMock()

        bank = Bank('test_updated_bank')
        self.manager.append(bank)
        self.controller.created(bank)

        self.notifier.register(observer)

        bank.name = 'test_updated_bank_new'
        self.controller.updated(bank)
        observer.on_bank_updated.assert_called_with(bank, UpdateType.UPDATED, index=bank.index, origin=self.manager, token=None)

        bank.name = 'test_updated_bank_new_new'
        self.controller.updated(bank, self.TOKEN)
        observer.on_bank_updated.assert_called_with(bank, UpdateType.UPDATED, index=bank.index, origin=self.manager, token=self.TOKEN)

        self.notifier.unregister(observer)

        self.manager.banks.remove(bank)

    def test_updated_not_added_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_not_added_bank')
        with self.assertRaises(BankError):
            self.controller.updated(bank)

        observer.on_bank_updated.assert_not_called()
        self.notifier.unregister(observer)

    def test_updated_current_bank(self):
        # Configure
        original_current_pedalboard = self.current.pedalboard

        bank = Bank('test_updated_current_bank 1')
        pedalboard1 = Pedalboard('test_updated_current_bank pedalboard')
        pedalboard2 = Pedalboard('test_updated_current_bank pedalboard2')
        bank.append(pedalboard1)
        bank.append(pedalboard2)

        bank2 = Bank('test_updated_current_bank 2')
        pedalboard3 = Pedalboard('test_updated_current_bank pedalboard3')
        pedalboard4 = Pedalboard('test_updated_current_bank pedalboard4')
        bank2.append(pedalboard3)
        bank2.append(pedalboard4)

        self.manager.append(bank)

        # Apply
        current_pedalboard = pedalboard1
        self.current.set_pedalboard(current_pedalboard)
        self.assertEqual(self.current.pedalboard, pedalboard1)
        self.assertEqual(self.current.bank, bank)

        self.manager.banks[bank.index] = bank2
        self.assertEqual(self.current.pedalboard, pedalboard1)
        self.assertEqual(self.current.bank, bank)

        # Only changes current pedalboard after notify current bank has updated
        self.controller.updated(bank2, current_bank=True)
        self.assertEqual(self.current.pedalboard, pedalboard3)
        self.assertEqual(self.current.bank, bank2)

        # Tear down
        self.current.set_pedalboard(original_current_pedalboard)
        self.manager.banks.remove(bank2)

    def test_deleted_bank(self):
        # Configure
        observer = MagicMock()
        total = len(self.controller.banks)

        bank = Bank('test_deleted_bank')

        self.manager.append(bank)
        self.controller.created(bank)

        self.notifier.register(observer)

        # Test
        self.assertLess(total, len(self.controller.banks))
        index = bank.index
        self.manager.banks.remove(bank)
        self.controller.deleted(bank, index)
        self.assertEqual(total, len(self.controller.banks))

        observer.on_bank_updated.assert_called_with(bank, UpdateType.DELETED, index=index, origin=self.manager, token=None)

        # Test 2
        bank2 = Bank('test_deleted_bank 2')
        self.manager.append(bank2)
        index = bank2.index
        self.controller.created(bank2)
        self.manager.banks.remove(bank2)
        self.controller.deleted(bank2, index, self.TOKEN)

        observer.on_bank_updated.assert_called_with(bank2, UpdateType.DELETED, index=index, origin=self.manager, token=self.TOKEN)
        self.notifier.unregister(observer)

    def test_deleted_bank_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_deleted_bank_error')
        self.manager.append(bank)
        with self.assertRaises(BankError):
            self.controller.deleted(bank, bank.index)

        observer.on_bank_updated.assert_not_called()
        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)

    def test_deleted_current_bank(self):
        original_current_pedalboard = self.current.pedalboard

        bank = Bank('test_deleted_current_bank 1')
        pedalboard1 = Pedalboard('test_deleted_current_bank pedalboard')
        pedalboard2 = Pedalboard('test_deleted_current_bank pedalboard2')
        bank.append(pedalboard1)
        bank.append(pedalboard2)

        bank2 = Bank('test_deleted_current_bank 2')
        pedalboard3 = Pedalboard('test_deleted_current_bank pedalboard3')
        pedalboard4 = Pedalboard('test_deleted_current_bank pedalboard4')
        bank2.append(pedalboard3)
        bank2.append(pedalboard4)

        self.manager.append(bank)
        self.manager.append(bank2)

        # Apply
        current_pedalboard = pedalboard1
        self.current.set_pedalboard(current_pedalboard)
        self.assertEqual(self.current.pedalboard, pedalboard1)
        self.assertEqual(self.current.bank, bank)

        old_index = bank.index
        self.manager.banks.remove(bank)
        self.assertEqual(self.current.pedalboard, pedalboard1)
        self.assertEqual(self.current.bank, bank)

        # Only changes current pedalboard after notify current bank has updated
        self.controller.deleted(bank, old_index)
        self.assertEqual(self.current.pedalboard, pedalboard3)
        self.assertEqual(self.current.bank, bank2)

        # Tear down
        self.current.set_pedalboard(original_current_pedalboard)
        self.manager.banks.remove(bank2)
