from controller.BanksController import BanksController
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.EffectController import EffectController
from controller.NotificationController import NotificationController
from controller.ParamController import ParamController
from controller.PatchController import PatchController
from controller.PluginsController import PluginsController


class Application(object):
    controllers = {}

    def __init__(self, data_patch="data/", address="localhost", test=False):
        self.dataPatch = data_patch

        controllers = [
            BanksController,
            CurrentController,
            EffectController,
            NotificationController,
            ParamController,
            PatchController,
            PluginsController
        ]

        self.controllers[DeviceController.__name__] = self.init_device_controller(address, test)

        for controller in controllers:
            self.controllers[controller.__name__] = controller(self)

        for controller in list(self.controllers.values()):
            controller.configure()

    def init_device_controller(self, address, test):
        if test:
            from unittest.mock import Mock
            return Mock(spec=DeviceController)

        else:
            device_controller = DeviceController(self)
            device_controller.address = address

            return device_controller

    def dao(self, dao):
        return dao(self.dataPatch)

    def controller(self, controller):
        return self.controllers[controller.__name__]


class ApplicationSingleton(object):
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Application(test=True)

        return cls.instance
