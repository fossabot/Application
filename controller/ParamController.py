# -*- coding: utf-8 -*-
from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController


class ParamController(Controller):

    def configure(self):
        from controller.CurrentController import CurrentController
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def updateValue(self, param, new_value, token=None):
        patch = param.effect.patch
        bank = patch.bank

        param.value = new_value

        self.dao.save(bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.updateParamValue(param)

        self.notificationController.notifyParamValueChange(param, token)
