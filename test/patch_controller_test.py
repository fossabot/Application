# -*- coding: utf-8 -*-
import unittest

from architecture.privatemethod import privatemethod

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

    @privatemethod
    def generate_patch(self, name):
        return {
            'name': name,
            'effects': [],
            'connections': []
        }

    def test_create_patch(self):
        json = self.generate_patch('test_create_patch')

        totalPatches = len(self.currentBank.patches)
        patchIndex = self.controller.createPatch(self.currentBank, json)
        patch = self.currentController.currentBank.patches[patchIndex]

        # Index is last patch + 1
        self.assertEqual(totalPatches, patchIndex)

        self.assertLess(totalPatches, len(self.currentBank.patches))

        self.controller.deletePatch(patch)

    def test_update_patch(self):
        newName = 'test_update_patch 2'
        json = self.generate_patch('test_update_patch')

        patchIndex = self.controller.createPatch(self.currentBank, json)
        patch = self.currentBank.patches[patchIndex]

        newPatchData = dict(self.currentController.currentPatch.json)
        newPatchData['name'] = newName

        self.controller.updatePatch(patch, newPatchData)

        self.assertEqual(patch['name'], newName)

        self.controller.deletePatch(patch)

    def test_update_current_patch(self):
        newName = 'test_update_current_patch 2'
        json = self.generate_patch('test_update_current_patch')

        patchIndex = self.controller.createPatch(self.currentBank, json)
        patch = self.currentBank.patches[patchIndex]

        self.currentController.setPatch(patchIndex)

        newPatchData = dict(self.currentController.currentPatch.json)
        newPatchData['name'] = newName

        self.controller.updatePatch(patch, newPatchData)

        self.assertEqual(patch['name'], newName)

        self.currentController.setPatch(0)  # Delete current patch is tested in another test
        self.controller.deletePatch(patch)

    def test_delete_patch(self):
        json = self.generate_patch('test_delete_patch')

        patchIndex = self.controller.createPatch(self.currentBank, json)
        patch = self.currentBank.patches[patchIndex]

        totalPatches = len(self.currentBank.patches)
        self.controller.deletePatch(patch)

        self.assertEqual(totalPatches - 1, len(self.currentBank.patches))

    def test_update_deleted_patch(self):
        #FIXME - Implement
        pass

    def test_delete_current_patch(self):
        json = self.generate_patch('test_delete_current_patch')

        patchIndex = self.controller.createPatch(self.currentBank, json)

        self.currentController.setPatch(patchIndex)

        totalPatches = len(self.currentBank.patches)
        self.controller.deletePatch(self.currentController.currentPatch)

        self.assertEqual(totalPatches-1, len(self.currentBank.patches))

        currentPatchNumber = self.currentController.patchNumber
        self.assertNotEqual(patchIndex, currentPatchNumber)
