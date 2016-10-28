# -*- coding: utf-8 -*-
from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController


class ParamController(Controller):
    """
    Manage :class:`Param`, updating your value
    """

    def configure(self):
        from controller.CurrentController import CurrentController
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def updateValue(self, param, new_value, token=None):
        """
        Set the value of a :class:`Param`.

        :param Param param: Effect parameter that will be changed your value
        :param new_value: New param value
        :param string token: Request token identifier
        """
        patch = param.effect.patch
        bank = patch.bank

        param.value = new_value

        self.dao.save(bank)

        if self.currentController.isCurrentPatch(patch):
            self.deviceController.updateParamValue(param)

        self.notificationController.notifyParamValueChange(param, token)
