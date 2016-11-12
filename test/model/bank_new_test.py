import unittest
from unittest.mock import MagicMock

from model.bank import Bank
from model.update_type import UpdateType


class BankTest(unittest.TestCase):

    def test_add_patch_by_patches(self):
        bank = Bank('Bank 1')

        patch1 = MagicMock()
        patch2 = MagicMock()

        bank.observer = MagicMock()

        bank.patches.append(patch1)
        self.assertEqual(patch1.bank, bank)
        self.assertEqual(bank.patches[0], patch1)
        bank.observer.onPatchUpdated.assert_called_with(patch1, UpdateType.CREATED)

        bank.patches.append(patch2)
        self.assertEqual(patch2.bank, bank)
        self.assertEqual(bank.patches[1], patch2)
        bank.observer.onPatchUpdated.assert_called_with(patch2, UpdateType.CREATED)

    def test_add_patch(self):
        bank = Bank('Bank 1')

        patch1 = MagicMock()
        patch2 = MagicMock()

        bank.observer = MagicMock()

        bank.append(patch1)
        self.assertEqual(patch1.bank, bank)
        self.assertEqual(bank.patches[0], patch1)
        bank.observer.onPatchUpdated.assert_called_with(patch1, UpdateType.CREATED)

        bank.append(patch2)
        self.assertEqual(patch2.bank, bank)
        self.assertEqual(bank.patches[1], patch2)
        bank.observer.onPatchUpdated.assert_called_with(patch2, UpdateType.CREATED)

    def test_update_patch(self):
        bank = Bank('Bank 1')

        patch1 = MagicMock()
        patch2 = MagicMock()

        bank.append(patch1)

        bank.observer = MagicMock()
        bank.patches[0] = patch2

        self.assertEqual(patch2.bank, bank)
        self.assertEqual(bank.patches[0], patch2)
        bank.observer.onPatchUpdated.assert_called_with(patch2, UpdateType.UPDATED)

    def test_delete_patch(self):
        bank = Bank('Bank 1')

        patch = MagicMock()

        bank.append(patch)

        bank.observer = MagicMock()
        del bank.patches[0]

        self.assertEqual(patch.bank, None)
        self.assertEqual(len(bank.patches), 0)
        bank.observer.onPatchUpdated.assert_called_with(patch, UpdateType.DELETED)
