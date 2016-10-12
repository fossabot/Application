# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

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
        self.controller = self._get_controller(NotificationController)
        self.currentController = self._get_controller(CurrentController)

    def _get_controller(self, controller):
        return NotificationControllerTest.application.controller(controller)

    def test_notify_current_patch_change(self):
        observer = Mock(spec=UpdatesObserver)
        self.controller.register(observer)

        self.currentController.toNextPatch()
        self.assertTrue(observer.onCurrentPatchChange.called, "Method onCurrentPatchChange called")

        observer.onCurrentPatchChange.reset_mock()
        self.currentController.toBeforePatch()
        observer.onCurrentPatchChange.assert_called_once_with(self.currentController.currentPatch, None)

        self.controller.unregister(observer)
