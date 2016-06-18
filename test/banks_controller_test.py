import unittest

from Application import ApplicationSingleton
from controller.BanksController import BanksController


class BanksControllerTest(unittest.TestCase):
    application = None
    controller = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()
        print("Loaded Application")

    def setUp(self):
        self.controller = BanksControllerTest.application.controller(
            BanksController
        )

        self.controller.setBank(0)
        self.controller.setPatch(0)

    def test_all_banks(self):
        self.assertIsNotNone(self.banks.all)
        self.assertNotEqual(0, len(self.banks.all))

    def test_create_bank(self):
        self.fail("Not implemented")

    def test_update_bank(self):
        self.fail("Not implemented")

    def test_create_patch(self):
        self.fail("Not implemented")

    def test_add_effect(self):
        self.fail("Not implemented")

    def test_delete_bank(self):
        self.fail("Not implemented")