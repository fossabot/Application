# -*- coding: utf-8 -*-
import unittest

from Application import ApplicationSingleton
from controller.BanksController import BanksController
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
            BanksController
        )

        currentController = BanksControllerTest.application.controller(
            CurrentController
        )

        currentController.setBank(0)
        currentController.setPatch(0)

    def test_all_banks(self):
        self.assertIsNotNone(self.controller.banks.all)
        self.assertNotEqual(0, len(self.controller.banks.all))

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