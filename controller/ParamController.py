# -*- coding: utf-8 -*-
from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController


class ParamController(Controller):

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def updateValue(self, effect, param, newValue):
        patch = effect.patch
        bank = patch.bank

        param['value'] = newValue

        self.dao.save(bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.loadPatch(patch)

        self.notificationController.notifyParamValueChange(
            bank.index,
            bank.indexOfPatch(patch),
            0,
            0
        )