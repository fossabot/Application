from controller.BanksController import BanksController
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.PluginsController import PluginsController


class Application:
    controllers = {}

    def __init__(self, dataPatch="data/"):
        self.dataPatch = dataPatch
        controllers = [
            BanksController,
            CurrentController,
            DeviceController,
            PluginsController
        ]

        for controller in controllers:
            self.controllers[controller.__name__] = controller(self)

        for controller in list(self.controllers.values()):
            controller.configure()

    def dao(self, dao):
        return dao(self.dataPatch)

    def controller(self, controller):
        return self.controllers[controller.__name__]