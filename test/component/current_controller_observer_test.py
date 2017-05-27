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

from application.component.current_pedalboard_observer import CurrentPedalboardObserver
from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from test.controller.controller_test import ControllerTest


class CurrentControllerObserverTest(ControllerTest):
    """
    Tests whether :class:`.ComponentController` is being called
    transparently through the changes made in the model classes.
    """

    def setUp(self):
        self._current = self.controller(CurrentController)
        self._notifier = self.controller(NotificationController)
        self._manager = self.controller(BanksController).manager

        self.original_current_pedalboard = self._current.pedalboard
        
        bank = self.generate_bank('A bank - CurrentControllerObserverTest')
        self._manager.append(bank)
        self._current.set_pedalboard(bank.pedalboards[0])
        
        self.observer = CurrentPedalboardObserver(self._current)
        self._manager.register(self.observer)

    def tearDown(self):
        self._manager.unregister(self.observer)
        self._current.set_pedalboard(self.original_current_pedalboard)
        
    def generate_bank(self, name):
        # Configure
        bank = Bank(name)
        pedalboard1 = Pedalboard(name + ' pedalboard')
        pedalboard2 = Pedalboard(name + ' pedalboard2')
        bank.append(pedalboard1)
        bank.append(pedalboard2)
        
        return bank

    def test_bank_updated(self):
        bank1 = self._current.bank
        bank2 = self.generate_bank('test_bank_updated')

        current_pedalboard = self._current.pedalboard

        # Change bank
        self._manager.banks[bank1.index] = bank2
        self.assertNotEqual(self._current.pedalboard, current_pedalboard)
        self.assertEqual(self._current.pedalboard, bank2.pedalboards[current_pedalboard.index])
        self.assertEqual(self._current.bank, bank2)

        # Tear down
        self._manager.banks.remove(bank2)

    def test_bank_updated_same_bank(self):
        bank1 = self._current.bank
        current_pedalboard = self._current.pedalboard

        # Change bank
        self._manager.banks[bank1.index] = bank1
        self.assertEqual(self._current.pedalboard, current_pedalboard)
        self.assertEqual(self._current.bank, bank1)

        # Tear down
        self._manager.banks.remove(bank1)

    def test_bank_deleted(self):
        bank1 = self._current.bank
        bank2 = self.generate_bank('test_bank_updated')

        self._manager.append(bank2)

        current_pedalboard = self._current.pedalboard

        # Delete current bank bank
        self._manager.banks.remove(bank1)

        self.assertEqual(self._current.pedalboard, bank2.pedalboards[current_pedalboard.index])
        self.assertEqual(self._current.bank, bank2)

        # Tear down
        self._manager.banks.remove(bank2)

    def test_pedalboard_updated(self):
        bank1 = self._current.bank

        current_pedalboard = self._current.pedalboard
        other_pedalboard = Pedalboard('Other pedalboard')

        # Change bank
        bank1.pedalboards[current_pedalboard.index] = other_pedalboard
        self.assertNotEqual(self._current.pedalboard, current_pedalboard)
        self.assertEqual(self._current.pedalboard, other_pedalboard)
        self.assertEqual(self._current.bank, bank1)

        # Tear down
        self._manager.banks.remove(bank1)

    def test_pedalboard_updated_same_pedalboard(self):
        bank1 = self._current.bank

        current_pedalboard = self._current.pedalboard

        # Change bank
        bank1.pedalboards[current_pedalboard.index] = current_pedalboard
        self.assertEqual(self._current.pedalboard, current_pedalboard)
        self.assertEqual(self._current.bank, bank1)

        # Tear down
        self._manager.banks.remove(bank1)
