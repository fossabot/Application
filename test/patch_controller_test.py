# -*- coding: utf-8 -*-
import unittest

from Application import ApplicationSingleton

from controller.PatchController import PatchController
from controller.CurrentController import CurrentController
from model.Patch import Patch


class PatchControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()

    def setUp(self):
        self.controller = PatchControllerTest.application.controller(
            PatchController
        )

        self.currentController = PatchControllerTest.application.controller(
            CurrentController
        )

        self.currentController.setBank(0)
        self.currentController.setPatch(0)

        self.currentBank = self.currentController.currentBank

    def test_create_patch(self):
        patch = {
            'name': 'test_create_patch',
            'effects': [],
            'connections': []
        }

        totalPatches = len(self.currentBank.patches)
        patchIndex = self.controller.createPatch(self.currentBank, patch)
        patch = self.currentController.currentBank.patches[patchIndex]

        # Index is last patch + 1
        self.assertEqual(totalPatches, patchIndex)

        self.assertLess(totalPatches, len(self.currentBank.patches))

        self.controller.deletePatch(patch)

    def test_update_patch(self):
        newName = 'test_update_patch 2'
        patchJson = {
            'name': 'test_update_patch',
            'effects': [],
            'connections': []
        }

        patchIndex = self.controller.createPatch(self.currentBank, patchJson)

        newPatchData = dict(self.currentController.currentPatch.json)
        newPatchData['name'] = newName

        patch = self.currentBank.patches[patchIndex]
        self.controller.updatePatch(patch, newPatchData)

        self.assertEqual(patch['name'], newName)

        self.controller.deletePatch(patch)

    def test_update_current_patch(self):
        newName = 'test_update_current_patch 2'
        patchJson = {
            'name': 'test_update_current_patch',
            'effects': [],
            'connections': []
        }

        patchIndex = self.controller.createPatch(self.currentBank, patchJson)
        self.currentController.setPatch(patchIndex)

        newPatchData = dict(self.currentController.currentPatch.json)
        newPatchData['name'] = newName

        patch = self.currentBank.patches[patchIndex]
        self.controller.updatePatch(patch, newPatchData)

        self.assertEqual(self.currentBank.patches[patchIndex]['name'], newName)

        self.currentController.setPatch(0) #  Delete current patch is tested in another test
        self.controller.deletePatch(patch)

    def test_delete_patch(self):
        patch = {
            'name': 'test_delete_patch',
            'effects': [],
            'connections': []
        }

        patchIndex = self.controller.createPatch(self.currentBank, patch)
        patch = self.currentBank.patches[patchIndex]

        totalPatches = len(self.currentBank.patches)
        self.controller.deletePatch(patch)

        self.assertEqual(totalPatches - 1, len(self.currentBank.patches))

    def test_update_deleted_patch(self):
        #FIXME - Implement
        pass

    def test_delete_current_patch(self):
        patch = {
            'name': 'test_delete_current_patch',
            'effects': [],
            'connections': []
        }

        patchIndex = self.controller.createPatch(self.currentBank, patch)

        self.currentController.setPatch(patchIndex)

        totalPatches = len(self.currentBank.patches)
        self.controller.deletePatch(self.currentController.currentPatch)

        self.assertEqual(totalPatches-1, len(self.currentBank.patches))

        self.assertNotEqual(
            patchIndex,
            self.currentController.patchNumber
        )
