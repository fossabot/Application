# -*- coding: utf-8 -*-
import unittest

from Application import ApplicationSingleton

from controller.PatchController import PatchController
from controller.CurrentController import CurrentController


class BanksControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()
        print("Loaded Application")

    def setUp(self):
        self.controller = BanksControllerTest.application.controller(
            PatchController
        )

        self.currentController = BanksControllerTest.application.controller(
            CurrentController
        )

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

        self.currentBank = self.currentController.getCurrentBank()

    def test_create_patch(self):
        patch = {
            'name': 'test_create_patch',
            'effects': [],
            'connections': []
        }

        totalPatches = len(self.currentBank.patches)
        patchIndex = self.controller.createPatch(self.currentBank, patch)

        # Index is last patch + 1
        self.assertEqual(totalPatches, patchIndex)

        self.assertLess(totalPatches, len(self.currentBank.patches))

        self.controller.deletePatch(self.currentBank, patchIndex)

    def test_update_patch(self):
        newName = 'test_update_patch 2'
        patch = {
            'name': 'test_update_patch',
            'effects': [],
            'connections': []
        }
        patchIndex = self.controller.createPatch(self.currentBank, patch)

        newPatchData = {}
        newPatchData.update(patch)
        newPatchData['name'] = newName

        self.controller.updatePatch(
            self.currentBank,
            patchIndex,
            newPatchData
        )

        self.assertEqual(self.currentBank.patches[patchIndex]['name'], newName)

        self.controller.deletePatch(self.currentBank, patchIndex)

    def test_update_out_range_patch(self):
        newPatchData = {
            'name': 'test_update_out_range_patch',
            'effects': [],
            'connections': []
        }

        with self.assertRaises(IndexError):
            self.controller.updatePatch(
                self.currentBank,
                5000,
                newPatchData
            )

    def test_delete_patch(self):
        patch = {
            'name': 'test_create_patch',
            'effects': [],
            'connections': []
        }

        patchIndex = self.controller.createPatch(self.currentBank, patch)

        totalPatches = len(self.currentBank.patches)
        self.controller.deletePatch(self.currentBank, patchIndex)

        self.assertEqual(totalPatches - 1, len(self.currentBank.patches))

    def test_delete_out_range_patch(self):
        with self.assertRaises(IndexError):
            self.controller.deletePatch(self.currentBank, 5000)
