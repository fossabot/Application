from controller.EffectController import EffectController
from controller.PluginsController import PluginsController
from controller.NotificationController import NotificationController

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch
from pluginsmanager.model.connection import Connection
from pluginsmanager.model.update_type import UpdateType
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

import unittest
from unittest.mock import MagicMock


class EffectControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'EFFECT_TOKEN'

        controller = EffectControllerTest.application.controller
        self.controller = controller(EffectController)
        self.plugins_controller = controller(PluginsController)
        self.notification_controller = controller(NotificationController)

        self.builder = Lv2EffectBuilder()

    def test_create_effect(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        bank = Bank('test_create_effect Bank')
        patch = Patch('test_create_effect Patch')
        bank.append(patch)
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        self.controller.create_effect(reverb)
        observer.on_effect_updated.assert_called_with(reverb, UpdateType.CREATED, None)

        self.controller.create_effect(reverb2, self.TOKEN)
        observer.on_effect_updated.assert_called_with(reverb2, UpdateType.CREATED, self.TOKEN)

        self.controller.delete_effect(reverb)
        self.controller.delete_effect(reverb2)

    def test_delete_effect(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        bank = Bank('test_create_effect Bank')
        patch = Patch('test_create_effect Patch')
        bank.append(patch)
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        self.controller.create_effect(reverb)
        self.controller.create_effect(reverb2)

        self.controller.delete_effect(reverb)
        observer.on_effect_updated.assert_called_with(reverb, UpdateType.DELETED, None)
        self.controller.delete_effect(reverb2, self.TOKEN)
        observer.on_effect_updated.assert_called_with(reverb2, UpdateType.DELETED, self.TOKEN)

    def test_toggle_status(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        bank = Bank('test_toggle_status Bank')
        patch = Patch('test_toggle_status Patch')
        bank.append(patch)
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        self.controller.create_effect(reverb)
        self.controller.create_effect(reverb2)

        self.controller.toggle_status(reverb)
        observer.on_effect_status_toggled.assert_called_with(reverb, None)

        self.controller.toggle_status(reverb2, self.TOKEN)
        observer.on_effect_status_toggled.assert_called_with(reverb2, self.TOKEN)

        self.controller.delete_effect(reverb)
        self.controller.delete_effect(reverb2, self.TOKEN)

    def test_connected(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        bank = Bank('test_connected Bank')
        patch = Patch('test_connected Patch')
        bank.append(patch)
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        self.controller.create_effect(reverb)
        self.controller.create_effect(reverb2)

        reverb.outputs[0].connect(reverb2.inputs[0])
        connection1 = patch.connections[-1]

        connection2 = Connection(reverb.outputs[1], reverb2.inputs[0])
        patch.connections.append(connection2)

        self.controller.connected(connection1)
        observer.on_connection_updated.assert_called_with(connection1, UpdateType.CREATED, None)

        self.controller.connected(connection2, self.TOKEN)
        observer.on_connection_updated.assert_called_with(connection2, UpdateType.CREATED, self.TOKEN)

        self.controller.delete_effect(reverb)
        self.controller.delete_effect(reverb2)

    def test_disconnected(self):
        observer = MagicMock()
        self.notification_controller.register(observer)

        bank = Bank('test_disconnected Bank')
        patch = Patch('test_disconnected Patch')
        bank.append(patch)
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        patch.append(reverb)
        patch.append(reverb2)

        self.controller.create_effect(reverb)
        self.controller.create_effect(reverb2)

        reverb.outputs[0].connect(reverb2.inputs[0])
        connection1 = patch.connections[-1]

        connection2 = Connection(reverb.outputs[1], reverb2.inputs[0])
        patch.connections.append(connection2)

        patch.connections.remove(connection1)
        self.controller.disconnected(connection1)
        observer.on_connection_updated.assert_called_with(connection1, UpdateType.DELETED, None)

        patch.connections.remove(connection2)
        self.controller.disconnected(connection2, self.TOKEN)
        observer.on_connection_updated.assert_called_with(connection2, UpdateType.DELETED, self.TOKEN)

        self.controller.delete_effect(reverb)
        self.controller.delete_effect(reverb2)

    @unittest.skip('Not implemented')
    def test_delete_effect_remove_connections(self):
        pass
