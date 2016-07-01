# -*- coding: utf-8 -*-
import unittest

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
        self.controller = CurrentControllerTest.application.controller(
            CurrentController
        )

        self.banksController = CurrentControllerTest.application.controller(
            BanksController
        )

        self.controller.setBank(0)
        self.controller.setPatch(0)

    def test_toggle_status_effects(self):
        effects = self.controller.getCurrentPatch()['effects']
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
        effect = self.controller.getCurrentPatch()['effects'][effectIndex]

        param = effect['ports']['control']['input'][paramIndex]
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

    def test_is_current(self):
        currentBank = self.controller.getCurrentBank()
        currentPatch = self.controller.getCurrentPatch()

        anotherBank = self.banksController.banks.all[-1]
        anotherPatch = anotherBank.patches[0]

        self.assertTrue(self.controller.isCurrent(currentBank, currentPatch))

        self.assertFalse(self.controller.isCurrent(anotherBank, currentPatch))
        self.assertFalse(self.controller.isCurrent(currentBank, anotherPatch))

    def test_get_effect_of_current_patch(self):
        for index in range(len(self.controller.getCurrentPatch()['effects'])):
            self.assertIsNotNone(self.controller.getEffectOfCurrentPatch(index))

    def test_get_index_out_effect_of_current_patch(self):
        with self.assertRaises(IndexError):
            self.controller.getEffectOfCurrentPatch(5000)

    def test_get_current_patch(self):
        currentBank = self.controller.getCurrentBank()
        currentPatch = self.controller.getCurrentPatch()

        self.assertIsNotNone(currentPatch)
        self.assertEqual(
            currentBank.patches[0],
            currentPatch
        )

    def test_get_current_bank(self):
        currentBank = self.controller.getCurrentBank()
        self.assertIsNotNone(self.controller.getCurrentBank())
        self.assertEqual(
            self.banksController.banks.all[0],
            currentBank
        )

    def test_to_before_patch(self):
        totalEffects = len(self.controller.getCurrentBank().patches)
        for idEffect in reversed(range(totalEffects)):
            self.controller.toBeforePatch()
            self.assertEqual(idEffect, self.controller.patchNumber)
        
    def test_next_patch(self):
        totalEffects = len(self.controller.getCurrentBank().patches)
        for idEffect in range(totalEffects):
            self.assertEqual(idEffect, self.controller.patchNumber)
            self.controller.toNextPatch()

        self.assertEqual(0, self.controller.patchNumber)

    def test_set_patch(self):
        firstPatch = self.controller.getCurrentPatch()

        self.controller.setPatch(1)
        self.assertEqual(1, self.controller.patchNumber)

        self.assertNotEqual(firstPatch, self.controller.getCurrentPatch())

    def test_set_index_out_patch(self):
        with self.assertRaises(IndexError):
            self.controller.setPatch(5000)

    def test_before_bank(self):
        banks = self.banksController.banks.all
        for bank in reversed(banks):
            self.controller.toBeforeBank()
            self.assertEqual(bank, self.controller.getCurrentBank())
        
    def test_next_bank(self):
        banks = self.banksController.banks.all
        for bank in banks:
            self.assertEqual(bank, self.controller.getCurrentBank())
            self.controller.toNextBank()

        self.assertEqual(banks[0], self.controller.getCurrentBank())

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
