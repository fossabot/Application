import unittest

from application.application import Application


class ControllerTest(unittest.TestCase):
    application = None

    @classmethod
    def setUpClass(cls):
        cls.application = Application(data_patch='test/data/', test=True)

    @classmethod
    def controller(cls, controller):
        return cls.application.controller(controller)
