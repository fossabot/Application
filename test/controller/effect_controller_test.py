from application.controller.banks_controller import BanksController
from application.controller.effect_controller import EffectController
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
        cls.banks = cls.controller(BanksController)
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

    def test_create_effect(self):
        bank = self._create_default_bank('test_create_effect')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        self.banks.create(bank)

        self.effects.created(reverb)
        self.observer.on_effect_updated.assert_called_with(reverb, UpdateType.CREATED, None, index=0, origin=pedalboard)

        self.effects.created(reverb2, self.TOKEN)
        self.observer.on_effect_updated.assert_called_with(reverb2, UpdateType.CREATED, self.TOKEN, index=1, origin=pedalboard)

        self.banks.delete(bank)

    def test_delete_effect(self):
        bank = self._create_default_bank('test_delete_effect')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        self.banks.create(bank)

        self.effects.delete(reverb)
        self.observer.on_effect_updated.assert_called_with(reverb, UpdateType.DELETED, None, index=0, origin=pedalboard)

        self.effects.delete(reverb2, self.TOKEN)
        self.observer.on_effect_updated.assert_called_with(reverb2, UpdateType.DELETED, self.TOKEN, index=0, origin=pedalboard)

        self.banks.delete(bank)

    def test_toggle_status(self):
        bank = self._create_default_bank('test_toggle_status')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        self.banks.create(bank)

        self.effects.toggle_status(reverb)
        self.observer.on_effect_status_toggled.assert_called_with(reverb, None)

        self.effects.toggle_status(reverb2, self.TOKEN)
        self.observer.on_effect_status_toggled.assert_called_with(reverb2, self.TOKEN)

        self.banks.delete(bank)

    def test_connected(self):
        bank = self._create_default_bank('test_connected')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        self.banks.create(bank)

        reverb.outputs[0].connect(reverb2.inputs[0])
        connection1 = pedalboard.connections[-1]

        connection2 = Connection(reverb.outputs[1], reverb2.inputs[0])
        pedalboard.connections.append(connection2)

        self.effects.connected(pedalboard, connection1)
        self.observer.on_connection_updated.assert_called_with(pedalboard, connection1, UpdateType.CREATED, None)

        self.effects.connected(pedalboard, connection2, self.TOKEN)
        self.observer.on_connection_updated.assert_called_with(pedalboard, connection2, UpdateType.CREATED, self.TOKEN)

        self.banks.delete(bank)

    def test_disconnected(self):
        bank = self._create_default_bank('test_disconnected')
        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects

        self.banks.create(bank)

        reverb.outputs[0].connect(reverb2.inputs[0])
        connection1 = pedalboard.connections[-1]

        connection2 = Connection(reverb.outputs[1], reverb2.inputs[0])
        pedalboard.connections.append(connection2)

        pedalboard.connections.remove(connection1)
        self.effects.disconnected(pedalboard, connection1)
        self.observer.on_connection_updated.assert_called_with(pedalboard, connection1, UpdateType.DELETED, None)

        pedalboard.connections.remove(connection2)
        self.effects.disconnected(pedalboard, connection2, self.TOKEN)
        self.observer.on_connection_updated.assert_called_with(pedalboard, connection2, UpdateType.DELETED, self.TOKEN)

        self.banks.delete(bank)

    @unittest.skip('Not implemented')
    def test_delete_effect_remove_connections(self):
        pass
