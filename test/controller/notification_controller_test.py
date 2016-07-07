# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from architecture.privatemethod import privatemethod

from Application import ApplicationSingleton

from controller.NotificationController import NotificationController
from controller.CurrentController import CurrentController

from model.UpdatesObserver import UpdatesObserver


class NotificationControllerTest(unittest.TestCase):
    application = None
    controller = None
    currentController = None

    @classmethod
    def setUpClass(cls):
        cls.application = ApplicationSingleton.getInstance()

    def setUp(self):
        self.controller = self.get_controller(NotificationController)
        self.currentController = self.get_controller(CurrentController)

    @privatemethod
    def get_controller(self, controller):
        return NotificationControllerTest.application.controller(controller)

    def test_notify_current_patch_change(self):
        observer = Mock(spec=UpdatesObserver)
        self.controller.register(observer)

        self.currentController.toNextPatch()

        observer.onCurrentPatchChange.assert_called_with(self.currentController.currentPatch)

        self.controller.unregister(observer)
        self.currentController.toBeforePatch()
