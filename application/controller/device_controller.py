from application.controller.controller import Controller
from pluginsmanager.model.system.system_effect import SystemEffect


class DeviceController(Controller):
    """
    Apply changes in the device (mod-host)
    """
    sys_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

    def __init__(self, application):
        super(DeviceController, self).__init__(application)

    def configure(self):
        from application.controller.banks_controller import BanksController
        banks_controller = self.app.controller(BanksController)

        banks_controller.manager.register(self.mod_host)

    @property
    def mod_host(self):
        return self.app.mod_host

    @property
    def patch(self):
        return self.mod_host.patch

    @patch.setter
    def patch(self, patch):
        self.mod_host.patch = patch
