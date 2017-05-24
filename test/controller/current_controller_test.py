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

from application.controller.current_controller import CurrentController, CurrentPedalboardError
from application.controller.banks_controller import BanksController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard

from test.controller.controller_test import ControllerTest

import unittest
from unittest.mock import MagicMock


class CurrentControllerTest(ControllerTest):
    def setUp(self):
        self.TOKEN = 'CURRENT_TOKEN'

        controller = CurrentControllerTest.application.controller
        self.current = controller(CurrentController)
        self.banks_controller = controller(BanksController)
        self.notifier = controller(NotificationController)

        first_pedalboard = self.banks_controller.banks[0].pedalboards[0]
        self.current.set_pedalboard(first_pedalboard)
        self.manager = self.banks_controller.manager

    @property
    def bank_with_pedalboard(self):
        bank = Bank('A bank')
        pedalboard = Pedalboard('A pedalboard')
        bank.append(pedalboard)

        return bank

    def test_pedalboard_property(self):
        current_bank = self.current.bank
        current_pedalboard = self.current.pedalboard

        self.assertIsNotNone(current_pedalboard)
        self.assertEqual(
            current_bank.pedalboards[0],
            current_pedalboard
        )

    def test_pedalboard_property2(self):
        another_bank = self.bank_with_pedalboard
        self.manager.append(another_bank)

        current_pedalboard = self.current.pedalboard
        another_pedalboard = another_bank.pedalboards[0]

        self.assertNotEqual(another_pedalboard, current_pedalboard)

        self.manager.banks.remove(another_bank)

    def test_bank_property(self):
        current_bank = self.current.bank

        self.assertIsNotNone(current_bank)
        self.assertEqual(
            self.banks_controller.banks[0],
            current_bank
        )

    def test_bank_property2(self):
        current_bank = self.current.bank
        another_bank = self.bank_with_pedalboard

        self.manager.append(another_bank)
        self.assertNotEqual(current_bank, another_bank)

        self.manager.banks.remove(another_bank)

    def test_set_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        pedalboard = Pedalboard('Other pedalboard')
        self.current.bank.append(pedalboard)

        original_pedalboard = self.current.pedalboard

        self.current.set_pedalboard(pedalboard)
        self.assertEqual(pedalboard, self.current.pedalboard)
        observer.on_current_pedalboard_changed.assert_called_with(pedalboard, None)

        self.assertNotEqual(original_pedalboard, self.current.pedalboard)

        self.current.set_pedalboard(original_pedalboard, self.TOKEN)
        self.assertEqual(original_pedalboard, self.current.pedalboard)
        observer.on_current_pedalboard_changed.assert_called_with(original_pedalboard, self.TOKEN)

        self.current.bank.pedalboards.remove(pedalboard)

        self.notifier.unregister(observer)

    def test_set_pedalboard_other_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_pedalboard
        self.manager.append(bank)

        original_pedalboard = self.current.pedalboard
        original_bank = self.current.bank

        self.current.set_pedalboard(bank.pedalboards[0])
        self.assertEqual(bank.pedalboards[0], self.current.pedalboard)
        self.assertEqual(bank, self.current.bank)
        observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], None)

        self.current.set_pedalboard(original_pedalboard, self.TOKEN)
        self.assertEqual(original_pedalboard, self.current.pedalboard)
        self.assertEqual(original_bank, self.current.bank)
        observer.on_current_pedalboard_changed.assert_called_with(original_pedalboard, self.TOKEN)

        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)

    def test_set_pedalboard_current_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        self.current.set_pedalboard(self.current.pedalboard)
        observer.on_current_pedalboard_changed.assert_not_called()

        self.notifier.unregister(observer)

    def test_set_pedalboard_not_added(self):
        with self.assertRaises(CurrentPedalboardError):
            self.current.set_pedalboard(Pedalboard('Empty pedalboard'))

    def test_set_none_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        original_pedalboard = self.current.pedalboard
        self.current.set_pedalboard(None)
        observer.on_current_pedalboard_changed.assert_called_with(None, None)

        # Don't notify if not changes
        self.current.set_pedalboard(original_pedalboard, token=self.TOKEN)

        self.current.set_pedalboard(None, token=self.TOKEN)
        observer.on_current_pedalboard_changed.assert_called_with(None, self.TOKEN)

        self.notifier.unregister(observer)

    def test_to_before_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        pedalboard = Pedalboard('Other pedalboard')
        self.current.bank.append(pedalboard)

        for pedalboard in reversed(self.current.bank.pedalboards):
            self.current.to_before_pedalboard()
            self.assertEqual(pedalboard, self.current.pedalboard)
            observer.on_current_pedalboard_changed.assert_called_with(pedalboard, None)

        for pedalboard in reversed(self.current.bank.pedalboards):
            self.current.to_before_pedalboard(self.TOKEN)
            self.assertEqual(pedalboard, self.current.pedalboard)
            observer.on_current_pedalboard_changed.assert_called_with(pedalboard, self.TOKEN)

        self.assertEqual(0, self.current.pedalboard.index)
        self.current.bank.pedalboards.remove(pedalboard)

        self.notifier.unregister(observer)

    def test_to_next_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        last_pedalboard = Pedalboard('Other pedalboard')
        self.current.bank.append(last_pedalboard)

        self.current.set_pedalboard(last_pedalboard)
        for pedalboard in self.current.bank.pedalboards:
            self.current.to_next_pedalboard()
            self.assertEqual(pedalboard, self.current.pedalboard)
            observer.on_current_pedalboard_changed.assert_called_with(pedalboard, None)

        self.current.set_pedalboard(last_pedalboard)
        for pedalboard in self.current.bank.pedalboards:
            self.current.to_next_pedalboard(self.TOKEN)
            self.assertEqual(pedalboard, self.current.pedalboard)
            observer.on_current_pedalboard_changed.assert_called_with(pedalboard, self.TOKEN)

        self.current.bank.pedalboards.remove(last_pedalboard)

        self.notifier.unregister(observer)

    def test_before_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        last_bank = self.bank_with_pedalboard
        self.manager.append(last_bank)

        for bank in reversed(self.manager.banks):
            self.current.to_before_bank()
            self.assertEqual(bank, self.current.bank)
            observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], None)

        for bank in reversed(self.manager.banks):
            self.current.to_before_bank(self.TOKEN)
            self.assertEqual(bank, self.current.bank)
            observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], self.TOKEN)

        self.manager.banks.remove(last_bank)
        self.notifier.unregister(observer)

    def test_next_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        last_bank = self.bank_with_pedalboard
        self.manager.append(last_bank)

        self.current.to_before_bank()
        for bank in self.banks_controller.banks:
            self.current.to_next_bank()
            self.assertEqual(bank, self.current.bank)
            observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], None)

        for bank in self.banks_controller.banks:
            self.current.to_next_bank(self.TOKEN)
            self.assertEqual(bank, self.current.bank)
            observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], self.TOKEN)

        self.manager.banks.remove(last_bank)
        self.notifier.unregister(observer)

    def test_set_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_pedalboard
        self.manager.append(bank)

        first_bank = self.current.bank

        self.current.set_bank(bank)
        self.assertEqual(bank, self.current.bank)
        self.assertEqual(bank.pedalboards[0], self.current.pedalboard)
        observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], None)

        self.current.set_bank(first_bank, self.TOKEN)
        observer.on_current_pedalboard_changed.assert_called_with(first_bank.pedalboards[0], self.TOKEN)

        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)

    def test_set_bank_not_added(self):
        bank = self.bank_with_pedalboard
        with self.assertRaises(CurrentPedalboardError):
            self.current.set_bank(bank)

    def test_set_bank_current_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        self.current.set_bank(self.current.bank)
        observer.on_current_pedalboard_changed.assert_not_called()

        self.notifier.unregister(observer)

    def test_set_bank_empty(self):
        observer = MagicMock()
        self.notifier.register(observer)

        original_bank = self.current.bank
        bank = Bank('Empty bank')
        self.manager.append(bank)

        self.current.set_bank(bank)
        observer.on_current_pedalboard_changed.assert_called_with(None, None)

        self.current.set_bank(original_bank, self.TOKEN)
        observer.on_current_pedalboard_changed.assert_called_with(None, self.TOKEN)

        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)

    @unittest.skip
    def test_load_wrong_pedalboard_index_error(self):
        """
        System needs start if current pedalboard defined in file not exists.
        (The file informs bank index and pedalboard index).
        """
        assert False
