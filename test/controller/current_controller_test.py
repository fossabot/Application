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

import unittest
from unittest.mock import MagicMock

from application.controller.current_controller import CurrentController, CurrentPedalboardError
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from test.controller.controller_test import ControllerTest


class CurrentControllerTest(ControllerTest):
    @classmethod
    def setUpClass(cls):
        super(CurrentControllerTest, cls).setUpClass()
        cls.TOKEN = 'EFFECT_TOKEN'

        cls._current = cls.controller(CurrentController)

        cls.manager = cls.application.manager

    def setUp(self):
        self._current.set_pedalboard(self._first_pedalboard)

        self.observer = MagicMock()
        self.application.components_observer.register(self.observer)

    def tearDown(self):
        self.application.components_observer.unregister(self.observer)

        self._current.set_pedalboard(self._first_pedalboard)

    @property
    def _first_pedalboard(self):
        return self.manager.banks[0].pedalboards[0]

    @property
    def bank_with_pedalboard(self):
        bank = Bank('A bank')
        pedalboard = Pedalboard('A pedalboard')
        bank.append(pedalboard)

        return bank

    def test_pedalboard_property(self):
        current_bank = self._current.bank
        current_pedalboard = self._current.pedalboard

        self.assertIsNotNone(current_pedalboard)
        self.assertEqual(
            current_bank.pedalboards[0],
            current_pedalboard
        )

    def test_pedalboard_property2(self):
        another_bank = self.bank_with_pedalboard
        self.manager.append(another_bank)

        current_pedalboard = self._current.pedalboard
        another_pedalboard = another_bank.pedalboards[0]

        self.assertNotEqual(another_pedalboard, current_pedalboard)

        self.manager.banks.remove(another_bank)

    def test_bank_property(self):
        current_bank = self._current.bank

        self.assertIsNotNone(current_bank)
        self.assertEqual(
            self.manager.banks[0],
            current_bank
        )

    def test_bank_property2(self):
        current_bank = self._current.bank
        another_bank = self.bank_with_pedalboard

        self.manager.append(another_bank)
        self.assertNotEqual(current_bank, another_bank)

        self.manager.banks.remove(another_bank)

    def test_set_pedalboard(self):
        pedalboard = Pedalboard('Other pedalboard')
        self._current.bank.append(pedalboard)

        original_pedalboard = self._current.pedalboard

        self._current.set_pedalboard(pedalboard)
        self.assertEqual(pedalboard, self._current.pedalboard)
        self.observer.on_current_pedalboard_changed.assert_called_with(pedalboard, token=None)

        self.assertNotEqual(original_pedalboard, self._current.pedalboard)

        self._current.set_pedalboard(original_pedalboard, self.TOKEN)
        self.assertEqual(original_pedalboard, self._current.pedalboard)
        self.observer.on_current_pedalboard_changed.assert_called_with(original_pedalboard, token=self.TOKEN)

        self._current.bank.pedalboards.remove(pedalboard)

    def test_set_pedalboard_other_bank(self):
        bank = self.bank_with_pedalboard
        self.manager.append(bank)

        original_pedalboard = self._current.pedalboard
        original_bank = self._current.bank

        self._current.set_pedalboard(bank.pedalboards[0])
        self.assertEqual(bank.pedalboards[0], self._current.pedalboard)
        self.assertEqual(bank, self._current.bank)
        self.observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], token=None)

        self._current.set_pedalboard(original_pedalboard, self.TOKEN)
        self.assertEqual(original_pedalboard, self._current.pedalboard)
        self.assertEqual(original_bank, self._current.bank)
        self.observer.on_current_pedalboard_changed.assert_called_with(original_pedalboard, token=self.TOKEN)

        self.manager.banks.remove(bank)

    def test_set_pedalboard_current_pedalboard(self):
        self._current.set_pedalboard(self._current.pedalboard)
        self.observer.on_current_pedalboard_changed.assert_not_called()

    def test_set_pedalboard_not_added(self):
        with self.assertRaises(CurrentPedalboardError):
            self._current.set_pedalboard(Pedalboard('Empty pedalboard'))

        self.observer.on_current_pedalboard_changed.assert_not_called()

    def test_set_none_pedalboard(self):
        original_pedalboard = self._current.pedalboard
        self._current.set_pedalboard(None)
        self.observer.on_current_pedalboard_changed.assert_called_with(None, token=None)

        # Don't notify if not changes
        self._current.set_pedalboard(original_pedalboard, token=self.TOKEN)

        self._current.set_pedalboard(None, token=self.TOKEN)
        self.observer.on_current_pedalboard_changed.assert_called_with(None, token=self.TOKEN)

    def test_to_before_pedalboard(self):
        pedalboard = Pedalboard('Other pedalboard')
        self._current.bank.append(pedalboard)

        for pedalboard in reversed(self._current.bank.pedalboards):
            self._current.to_before_pedalboard()
            self.assertEqual(pedalboard, self._current.pedalboard)
            self.observer.on_current_pedalboard_changed.assert_called_with(pedalboard, token=None)

        for pedalboard in reversed(self._current.bank.pedalboards):
            self._current.to_before_pedalboard(self.TOKEN)
            self.assertEqual(pedalboard, self._current.pedalboard)
            self.observer.on_current_pedalboard_changed.assert_called_with(pedalboard, token=self.TOKEN)

        self.assertEqual(0, self._current.pedalboard.index)
        self._current.bank.pedalboards.remove(pedalboard)

    def test_to_before_pedalboard_error(self):
        self.execute_change_pedalboard_none_error(self._current.to_before_pedalboard)

    def execute_change_pedalboard_none_error(self, method):
        original_pedalboard = self._current.pedalboard

        self._current.set_pedalboard(None)
        self.observer.reset_mock()
        with self.assertRaises(CurrentPedalboardError):
            method()

        self.observer.on_current_pedalboard_changed.assert_not_called()
        self._current.set_pedalboard(original_pedalboard)

    def test_to_next_pedalboard(self):
        last_pedalboard = Pedalboard('Other pedalboard')
        self._current.bank.append(last_pedalboard)

        self._current.set_pedalboard(last_pedalboard)
        for pedalboard in self._current.bank.pedalboards:
            self._current.to_next_pedalboard()
            self.assertEqual(pedalboard, self._current.pedalboard)
            self.observer.on_current_pedalboard_changed.assert_called_with(pedalboard, token=None)

        self._current.set_pedalboard(last_pedalboard)
        for pedalboard in self._current.bank.pedalboards:
            self._current.to_next_pedalboard(self.TOKEN)
            self.assertEqual(pedalboard, self._current.pedalboard)
            self.observer.on_current_pedalboard_changed.assert_called_with(pedalboard, token=self.TOKEN)

        self._current.bank.pedalboards.remove(last_pedalboard)

    def test_to_next_pedalboard_error(self):
        self.execute_change_pedalboard_none_error(self._current.to_next_pedalboard)

    def test_before_bank(self):
        last_bank = self.bank_with_pedalboard
        self.manager.append(last_bank)

        for bank in reversed(self.manager.banks):
            self._current.to_before_bank()
            self.assertEqual(bank, self._current.bank)
            self.observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], token=None)

        for bank in reversed(self.manager.banks):
            self._current.to_before_bank(self.TOKEN)
            self.assertEqual(bank, self._current.bank)
            self.observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], token=self.TOKEN)

        self.manager.banks.remove(last_bank)

    def test_to_before_bank_error(self):
        self.execute_change_pedalboard_none_error(self._current.to_before_bank)

    def test_next_bank(self):
        last_bank = self.bank_with_pedalboard
        self.manager.append(last_bank)

        self._current.to_before_bank()
        for bank in self.manager.banks:
            self._current.to_next_bank()
            self.assertEqual(bank, self._current.bank)
            self.observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], token=None)

        for bank in self.manager.banks:
            self._current.to_next_bank(self.TOKEN)
            self.assertEqual(bank, self._current.bank)
            self.observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], token=self.TOKEN)

        self.manager.banks.remove(last_bank)

    def test_to_next_bank_error(self):
        self.execute_change_pedalboard_none_error(self._current.to_next_bank)

    def test_set_bank(self):
        bank = self.bank_with_pedalboard
        self.manager.append(bank)

        first_bank = self._current.bank

        self._current.set_bank(bank)
        self.assertEqual(bank, self._current.bank)
        self.assertEqual(bank.pedalboards[0], self._current.pedalboard)
        self.observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], token=None)

        self._current.set_bank(first_bank, self.TOKEN)
        self.observer.on_current_pedalboard_changed.assert_called_with(first_bank.pedalboards[0], token=self.TOKEN)

        self.manager.banks.remove(bank)

    def test_set_bank_not_added(self):
        bank = self.bank_with_pedalboard
        with self.assertRaises(CurrentPedalboardError):
            self._current.set_bank(bank)

    def test_set_bank_current_bank(self):
        self._current.set_bank(self._current.bank)
        self.observer.on_current_pedalboard_changed.assert_not_called()

    def test_set_bank_empty(self):
        original_bank = self._current.bank
        bank = Bank('Empty bank')
        self.manager.append(bank)

        self._current.set_bank(bank)
        self.observer.on_current_pedalboard_changed.assert_called_with(None, token=None)

        # Don't notify if not changes
        self._current.set_bank(original_bank, self.TOKEN)

        self._current.set_bank(bank, self.TOKEN)
        self.observer.on_current_pedalboard_changed.assert_called_with(None, token=self.TOKEN)

        self.manager.banks.remove(bank)

    @unittest.skip
    def test_load_wrong_pedalboard_index_error(self):
        """
        System needs start if current pedalboard defined in file not exists.
        (The file informs bank index and pedalboard index).
        """
        assert False
