import unittest

from Application import ApplicationSingleton
from controller.CurrentController import CurrentController


class CurrentControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()
        print("Loaded Application")

    def setUp(self):
        self.controller = CurrentControllerTest.application.controller(
            CurrentController
        )

        self.controller.setBank(0)
        self.controller.setPatch(0)

    def test_toggle_status_fitst_effect(self):
        self.fail("Not implemented")

    def test_toggle_status_effect_last(self):
        self.fail("Not implemented")

    def test_toggle_status_index_out_effect(self):
        self.fail("Not implemented")

    def test_set_effect_param(self):
        self.fail("Not implemented")

    def test_set_effect_param_invalid_value(self):
        self.fail("Not implemented")

    def test_set_effect_endex_out_param(self):
        self.fail("Not implemented")

    def test_get_effect_of_current_patch(self):
        self.assertIsNotNone(self.controller.getEffectOfCurrentPatch(0))
        self.assertIsNotNone(self.controller.getEffectOfCurrentPatch(1))

    def test_get_index_out_effect_of_current_patch(self):
        with self.assertRaises(IndexError):
            self.controller.getEffectOfCurrentPatch(5000)

    def test_get_current_patch(self):
        currentPatch = self.controller.getCurrentPatch()
        self.assertIsNotNone(currentPatch)

    def test_get_current_bank(self):
        self.assertIsNotNone(self.controller.getCurrentBank())

    def test_set_patch(self):
        firstPatch = self.controller.getCurrentPatch()

        self.controller.setPatch(1)
        self.assertEqual(1, self.controller.patchNumber)

        self.assertNotEqual(firstPatch, self.controller.getCurrentPatch())

    def test_set_index_out_patch(self):
        with self.assertRaises(IndexError):
            self.controller.setPatch(5000)

    def test_set_bank(self):
        firstBank = self.controller.getCurrentBank()

        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bankNumber)

        self.assertNotEqual(firstBank, self.controller.getCurrentBank())

    def test_setting_bank_patch_will_be_first(self):
        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bankNumber)
        self.assertEqual(0, self.controller.patchNumber)

    def test_set_index_out_bank(self):
        with self.assertRaises(IndexError):
            self.controller.setBank(5000)
