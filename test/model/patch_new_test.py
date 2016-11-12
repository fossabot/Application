import unittest
from unittest.mock import MagicMock

from model.patch import Patch
from model.update_type import UpdateType


class PatchTest(unittest.TestCase):

    def test_add_effect_by_effects(self):
        patch = Patch('Patch 1')

        effect1 = MagicMock()
        effect2 = MagicMock()

        patch.observer = MagicMock()

        patch.effects.append(effect1)
        self.assertEqual(effect1.patch, patch)
        self.assertEqual(patch.effects[0], effect1)
        patch.observer.onEffectUpdated.assert_called_with(effect1, UpdateType.CREATED)

        patch.effects.append(effect2)
        self.assertEqual(effect2.patch, patch)
        self.assertEqual(patch.effects[1], effect2)
        patch.observer.onEffectUpdated.assert_called_with(effect2, UpdateType.CREATED)

    def test_add_effect(self):
        patch = Patch('Patch 1')

        effect1 = MagicMock()
        effect2 = MagicMock()

        patch.observer = MagicMock()

        patch.append(effect1)
        self.assertEqual(effect1.patch, patch)
        self.assertEqual(patch.effects[0], effect1)
        patch.observer.onEffectUpdated.assert_called_with(effect1, UpdateType.CREATED)

        patch.append(effect2)
        self.assertEqual(effect2.patch, patch)
        self.assertEqual(patch.effects[1], effect2)
        patch.observer.onEffectUpdated.assert_called_with(effect2, UpdateType.CREATED)

    def test_update_effect(self):
        patch = Patch('Patch 1')

        effect1 = MagicMock()
        effect2 = MagicMock()

        patch.append(effect1)

        patch.observer = MagicMock()
        patch.effects[0] = effect2

        self.assertEqual(effect2.patch, patch)
        self.assertEqual(patch.effects[0], effect2)
        patch.observer.onEffectUpdated.assert_called_with(effect2, UpdateType.UPDATED)

    def test_delete_effect(self):
        patch = Patch('Bank 1')

        effect = MagicMock()

        patch.append(effect)

        patch.observer = MagicMock()
        del patch.effects[0]

        self.assertEqual(effect.patch, None)
        self.assertEqual(len(patch.effects), 0)
        patch.observer.onEffectUpdated.assert_called_with(effect, UpdateType.DELETED)

    def test_add_connection_by_connections(self):
        """ Other mode is by output.connect(input)"""
        patch = Patch('Patch 1')

        connection1 = MagicMock()
        connection2 = MagicMock()

        patch.observer = MagicMock()

        patch.connections.append(connection1)
        self.assertEqual(patch.connections[0], connection1)
        patch.observer.onConnectionUpdated.assert_called_with(connection1, UpdateType.CREATED)

        patch.connections.append(connection2)
        self.assertEqual(patch.connections[1], connection2)
        patch.observer.onConnectionUpdated.assert_called_with(connection2, UpdateType.CREATED)

    def test_update_connection(self):
        patch = Patch('Patch 1')

        connection1 = MagicMock()
        connection2 = MagicMock()

        patch.connections.append(connection1)

        patch.observer = MagicMock()
        patch.connections[0] = connection2

        self.assertEqual(patch.connections[0], connection2)
        patch.observer.onConnectionUpdated.assert_called_with(connection2, UpdateType.UPDATED)

    def test_delete_connection(self):
        """ Other mode is by output.disconnect(input)"""
        patch = Patch('Bank 1')

        connection = MagicMock()

        patch.connections.append(connection)

        patch.observer = MagicMock()
        del patch.connections[0]

        self.assertEqual(len(patch.connections), 0)
        patch.observer.onConnectionUpdated.assert_called_with(connection, UpdateType.DELETED)
