import unittest

from Application import Application
from controller.BanksController import BanksController


class BanksControlerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = Application()
        print("Loaded Application")

    def setUp(self):
        self.controller = BanksControllerTest.application.controller(BanksController)

        self.controller.setBank(0)
        self.controller.setPatch(0)

    def allBanks(self):
        self.assertIsNotNone(self.banks.all)
        self.assertNotEqual(0, len(self.banks.all))

    def createBank(self):
        pass

    def testupdateBank(self):
        pass

    def testCreatePatch(self):
        pass

    def testAddEffect(self):
        pass

    def deleteBank(self):

