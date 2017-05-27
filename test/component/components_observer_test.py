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

from unittest.mock import MagicMock

from application.component.components_observer import ComponentsObserver
from application.component.application_observer import ApplicationObserver
from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.observer.update_type import UpdateType
from test.controller.controller_test import ControllerTest


class MockObserver(ApplicationObserver):

    def __init__(self):
        super().__init__()

    def on_current_pedalboard_changed(self, pedalboard, **kwargs):
        pass

    def on_effect_status_toggled(self, effect, **kwargs):
        pass

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        pass

    def on_bank_updated(self, bank, update_type, index, origin, **kwargs):
        pass

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        pass

    def on_param_value_changed(self, param, **kwargs):
        pass

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        pass


class ComponentsObserverTest(ControllerTest):

    def generate_bank(self, name):
        # Configure
        bank = Bank(name)
        pedalboard1 = Pedalboard(name + ' pedalboard')
        pedalboard2 = Pedalboard(name + ' pedalboard2')
        bank.append(pedalboard1)
        bank.append(pedalboard2)
        
        return bank

    def test_notification(self):
        observer = MockObserver()
        observer.on_bank_updated = MagicMock()

        manager = BanksManager()
        components_observer = ComponentsObserver(manager)

        manager.register(components_observer)
        components_observer.register(observer)

        bank = self.generate_bank('test_notification')
        manager.append(bank)

        observer.on_bank_updated.assert_called_with(bank, UpdateType.CREATED, index=bank.index, origin=manager)

    def test_notification_scope(self):
        observer = MockObserver()
        observer.on_bank_updated = MagicMock()

        manager = BanksManager()
        components_observer = ComponentsObserver(manager)

        manager.register(components_observer)
        components_observer.register(observer)

        bank = self.generate_bank('test_notification')
        with observer:
            manager.append(bank)

        observer.on_bank_updated.assert_not_called()
