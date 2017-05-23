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

from application.controller.effect_controller import EffectController, EffectError, PedalboardConnectionError
from application.controller.notification_controller import NotificationController
from application.controller.plugins_controller import PluginsController

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.connection import Connection
from pluginsmanager.model.update_type import UpdateType

import unittest
from unittest.mock import MagicMock


class EffectControllerTest(ControllerTest):

    @classmethod
    def setUpClass(cls):
        super(EffectControllerTest, cls).setUpClass()

        cls.TOKEN = 'EFFECT_TOKEN'

        cls.effects = cls.controller(EffectController)
        cls.notifier = cls.controller(NotificationController)

        cls.plugins = cls.controller(PluginsController)

    def setUp(self):
        self.observer = MagicMock()
        self.notifier.register(self.observer)

    def tearDown(self):
        self.notifier.unregister(self.observer)

    def _create_default_bank(self, name):
        bank = Bank(name + ' Bank')
        pedalboard = Pedalboard(name + ' Pedalboard')

        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')

        bank.append(pedalboard)

        pedalboard.append(reverb)
        pedalboard.append(reverb2)

        return bank

    def test_created_effect(self):
        bank = self._create_default_bank('test_created_effect')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        self.effects.created(reverb)
        self.observer.on_effect_updated.assert_called_with(reverb, UpdateType.CREATED, token=None, index=0, origin=pedalboard)

        self.effects.created(reverb2, self.TOKEN)
        self.observer.on_effect_updated.assert_called_with(reverb2, UpdateType.CREATED, token=self.TOKEN, index=1, origin=pedalboard)

    def test_created_effect_error(self):
        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')

        with self.assertRaises(EffectError):
            self.effects.created(reverb)

        self.observer.on_effect_updated.assert_not_called()

    def test_deleted_effect(self):
        bank = self._create_default_bank('test_deleted_effect')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        old_index = reverb.index

        pedalboard.effects.remove(reverb)
        self.effects.deleted(reverb, old_index, pedalboard)
        self.observer.on_effect_updated.assert_called_with(reverb, UpdateType.DELETED, token=None, index=old_index, origin=pedalboard)

        old_index = reverb2.index

        pedalboard.effects.remove(reverb2)
        self.effects.deleted(reverb2, old_index, pedalboard, self.TOKEN)
        self.observer.on_effect_updated.assert_called_with(reverb2, UpdateType.DELETED, token=self.TOKEN, index=old_index, origin=pedalboard)

    def test_deleted_effect_error(self):
        pedalboard = Pedalboard('test_deleted_effect_error pedalboard')
        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)

        with self.assertRaises(EffectError):
            self.effects.deleted(reverb, 0, pedalboard)

        self.observer.on_effect_updated.assert_not_called()

    def test_toggled_status(self):
        bank = self._create_default_bank('test_toggled_status')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        reverb.toggle()
        self.effects.toggled_status(reverb)
        self.observer.on_effect_status_toggled.assert_called_with(reverb, None)

        reverb.toggle()
        self.effects.toggled_status(reverb2, self.TOKEN)
        self.observer.on_effect_status_toggled.assert_called_with(reverb2, self.TOKEN)

    def test_deleted_toggled_status_error(self):
        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')

        with self.assertRaises(EffectError):
            self.effects.toggled_status(reverb)

        self.observer.on_effect_updated.assert_not_called()

    def test_connected(self):
        bank = self._create_default_bank('test_connected')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        reverb.outputs[0].connect(reverb2.inputs[0])
        connection1 = pedalboard.connections[-1]

        connection2 = Connection(reverb.outputs[1], reverb2.inputs[0])
        pedalboard.connections.append(connection2)

        self.effects.connected(pedalboard, connection1)
        self.observer.on_connection_updated.assert_called_with(connection1, UpdateType.CREATED, pedalboard=pedalboard, token=None)

        self.effects.connected(pedalboard, connection2, self.TOKEN)
        self.observer.on_connection_updated.assert_called_with(connection2, UpdateType.CREATED, pedalboard=pedalboard, token=self.TOKEN)

    def test_connected_error(self):
        pedalboard = Pedalboard('test_connected_error pedalboard')

        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')

        connection = Connection(reverb.outputs[0], reverb2.inputs[0])
        with self.assertRaises(PedalboardConnectionError):
            self.effects.connected(pedalboard, connection)

        self.observer.on_effect_updated.assert_not_called()

    def test_disconnected(self):
        bank = self._create_default_bank('test_disconnected')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        reverb.outputs[0].connect(reverb2.inputs[0])
        connection1 = pedalboard.connections[-1]

        connection2 = Connection(reverb.outputs[1], reverb2.inputs[0])
        pedalboard.connections.append(connection2)

        pedalboard.connections.remove(connection1)
        self.effects.disconnected(pedalboard, connection1)
        self.observer.on_connection_updated.assert_called_with(connection1, UpdateType.DELETED, pedalboard=pedalboard, token=None)

        pedalboard.connections.remove(connection2)
        self.effects.disconnected(pedalboard, connection2, self.TOKEN)
        self.observer.on_connection_updated.assert_called_with(connection2, UpdateType.DELETED, pedalboard=pedalboard, token=self.TOKEN)

    def test_disconnected_error(self):
        pedalboard = Pedalboard('test_disconnected_error pedalboard')

        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')

        connection = Connection(reverb.outputs[0], reverb2.inputs[0])
        pedalboard.connections.append(connection)

        with self.assertRaises(PedalboardConnectionError):
            self.effects.disconnected(pedalboard, connection)

        self.observer.on_effect_updated.assert_not_called()
