import unittest

class CurrentControllerTest(unittest.TestCase):
    application = None
    controller = None

    def setUp(self):
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
