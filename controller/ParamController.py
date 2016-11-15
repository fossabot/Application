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
        self.current_controller = self.app.controller(CurrentController)
        self.device_controller = self.app.controller(DeviceController)
        self.notifier = self.app.controller(NotificationController)

    def updated_value(self, param, token=None):
        """
        Informs the :class:`Param` are updated.

        :param Param param: Effect parameter with your value changed
        :param string token: Request token identifier
        """
        # self.dao.save(param.effect.patch.bank)

        # if self.current_controller.isCurrentPatch(patch):
        #    self.device_controller.updateParamValue(param)

        self.notifier.param_value_changed(param, token)
