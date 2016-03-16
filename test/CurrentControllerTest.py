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
        
    def testSetBank(self):
        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bank)
        
    def testSetBankWithPatchDefaultFirst(self):
        self.controller.setBank(1)
        self.controller.setPatch(0)
        
        self.controller.setBank(1)
        self.assertEqual(1, self.controller.bank)
        self.assertEqual(0, self.controller.patch)

    def testToggleFirstStatusFitst(self):
        pass
    
    def testToggleStatusEffectLast(self):
        pass
    
    def testToggleStatusEffectIndexOut(self):
        pass
    
    def setEffectParam(self):
        pass
        
    def setEffectParamInvalidValue(self):
        pass
    
    def setEffectParamIndexOut(self):
        pass
