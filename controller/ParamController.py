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

    def updateValue(self, bank, patch, param, newValue):
        param['value'] = newValue

        self.dao.save(bank)

        if self.currentController.isCurrent(bank, patch):
            self.deviceController.loadPatch(
                self.currentController.getCurrentPatch()
            )

        self.notificationController.notifyParamValueChange(
            bank['index'],
            bank.patches.index(patch),
            effectIndex,
            paramIndex
        )