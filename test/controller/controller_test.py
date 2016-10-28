import unittest

from Application import Application


class ControllerTest(unittest.TestCase):
    application = None

    @classmethod
    def setUpClass(cls):
        cls.application = Application(test=True)
