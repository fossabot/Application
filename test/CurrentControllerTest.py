import unittest

from Application import Application
from controller.CurrentController import CurrentController


class CurrentControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = Application()
        print("Loaded Application")

    def setUp(self):
        self.controller = CurrentControllerTest.application.controller(CurrentController)

        self.controller.setBank(0)
        self.controller.setPatch(0)

    def toggleStatusFitstEffect(self):
        pass

    def toggleStatusEffectLast(self):
        pass

    def toggleStatusIndexOutEffect(self):
        pass

    def setEffectParam(self):
        pass

    def setEffectParamInvalidValue(self):
        pass

    def setEffectIndexOutParam(self):
        pass

    def getEffectOfCurrentPatch(self):
        self.assertIsNotNone(self.controller.getEffectOfCurrentPatch(0))
        self.assertIsNotNone(self.controller.getEffectOfCurrentPatch(1))

    def getIndexOutEffectOfCurrentPatch(self):
        with self.assertRaises(IndexError):
            self.controller.getEffectOfCurrentPatch(5000)

    def getCurrentPatch(self):
        currentPatch = self.controller.getCurrentPatch()
        self.assertIsNotNone(currentPatch)

    def getCurrentBank(self):
        self.assertIsNotNone(self.controller.getCurrentBank())

    def setPatch(self):
        firstPatch = self.controller.getCurrentPatch()

        self.controller.setPatch(1)
        self.assertEqual(1, self.controller.patchNumber)

        self.assertNotEqual(firstPatch, self.controller.getCurrentPatch())

    def setIndexOutPatch(self):
        with self.assertRaises(IndexError):
            self.controller.setPatch(5000)

    def setBank(self):
        firstBank = self.controller.getCurrentBank()

        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bankNumber)

        self.assertNotEqual(firstBank, self.controller.getCurrentBank())

    def testSettingBankPatchWillBeFirst(self):
        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bankNumber)
        self.assertEqual(0, self.controller.patchNumber)

    def setIndexOutBank(self):
        with self.assertRaises(IndexError):
            self.controller.setBank(5000)
