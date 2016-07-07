# -*- coding: utf-8 -*-
import unittest

from architecture.privatemethod import privatemethod

from Application import ApplicationSingleton
from controller.CurrentController import CurrentController
from controller.BanksController import BanksController


class CurrentControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()

    def setUp(self):
        self.controller = self.get_controller(CurrentController)
        self.banksController = self.get_controller(BanksController)

        self.controller.setBank(0)
        self.controller.setPatch(0)

    @privatemethod
    def get_controller(self, controller):
        return CurrentControllerTest.application.controller(controller)

    def test_current_patch(self):
        currentBank = self.controller.currentBank
        currentPatch = self.controller.currentPatch

        self.assertIsNotNone(currentPatch)
        self.assertEqual(
            currentBank.patches[0],
            currentPatch
        )

    def test_current_bank(self):
        currentBank = self.controller.currentBank
        self.assertIsNotNone(self.controller.currentBank)
        self.assertEqual(
            self.banksController.banks.all[0],
            currentBank
        )

    def test_toggle_status_effects(self):
        effects = self.controller.currentPatch.effects

        for index in range(len(effects)):
            effect = effects[index]
            actived = effect['status']

            self.controller.toggleStatusEffect(index)
            self.assertEqual(not actived, effect['status'])

            # Changing to original state
            self.controller.toggleStatusEffect(index)

    def test_toggle_status_index_out_effect(self):
        with self.assertRaises(IndexError):
            self.controller.toggleStatusEffect(5000)

    def test_set_effect_param(self):
        effectIndex = 0
        paramIndex = 0
        effect = self.controller.currentPatch.effects[effectIndex]

        param = effect.params[paramIndex]

        originalValue = param['value']
        newValue = originalValue+1

        self.controller.setEffectParam(effectIndex, paramIndex, newValue)

        self.assertEqual(newValue, param['value'])
        self.controller.setEffectParam(effectIndex, paramIndex, originalValue)

    '''
    def test_set_effect_param_invalid_value_min(self):
        self.fail("Not implemented")

    def test_set_effect_param_invalid_value_max(self):
        self.fail("Not implemented")
    '''

    def test_set_param_of_index_out_effect(self):
        with self.assertRaises(IndexError):
            self.controller.setEffectParam(5000, 0, 0)

    def test_set_param_of_index_out_param(self):
        with self.assertRaises(IndexError):
            self.controller.setEffectParam(0, 5000, 0)

    def test_is_current_patch(self):
        currentPatch = self.controller.currentPatch

        anotherBank = self.banksController.banks.all[-1]
        anotherPatch = anotherBank.patches[0]

        self.assertTrue(self.controller.isCurrentPatch(currentPatch))
        self.assertFalse(self.controller.isCurrentPatch(anotherPatch))

    def test_is_current_bank(self):
        currentBank = self.controller.currentBank
        anotherBank = self.banksController.banks.all[-1]

        self.assertTrue(self.controller.isCurrentBank(currentBank))
        self.assertFalse(self.controller.isCurrentBank(anotherBank))

    def test_to_before_patch(self):
        totalPatches = len(self.controller.currentBank.patches)
        for idPatch in reversed(range(totalPatches)):
            self.controller.toBeforePatch()
            self.assertEqual(idPatch, self.controller.patchNumber)

    def test_next_patch(self):
        totalPatches = len(self.controller.currentBank.patches)
        for idPatch in range(totalPatches):
            self.assertEqual(idPatch, self.controller.patchNumber)
            self.controller.toNextPatch()

        self.assertEqual(0, self.controller.patchNumber)

    def test_set_patch(self):
        firstPatch = self.controller.currentPatch

        self.controller.setPatch(1)
        self.assertEqual(1, self.controller.patchNumber)

        self.assertNotEqual(firstPatch, self.controller.currentPatch)

    def test_set_index_out_patch(self):
        with self.assertRaises(IndexError):
            self.controller.setPatch(5000)

    def test_before_bank(self):
        banks = self.banksController.banks.all
        for bank in reversed(banks):
            self.controller.toBeforeBank()
            self.assertEqual(bank, self.controller.currentBank)

    def test_next_bank(self):
        banks = self.banksController.banks.all
        for bank in banks:
            self.assertEqual(bank, self.controller.currentBank)
            self.controller.toNextBank()

        self.assertEqual(banks[0], self.controller.currentBank)

    def test_set_bank(self):
        firstBank = self.controller.currentBank

        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bankNumber)

        self.assertNotEqual(firstBank, self.controller.currentBank)

    def test_setting_bank_patch_will_be_first(self):
        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bankNumber)
        self.assertEqual(0, self.controller.patchNumber)

    def test_set_index_out_bank(self):
        with self.assertRaises(IndexError):
            self.controller.setBank(5000)
