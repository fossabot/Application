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

    def __init__(self, test=False, dataPatch="data/"):
        self.dataPatch = dataPatch
        controllers = [
            BanksController,
            CurrentController,
            DeviceController,
            EffectController,
            NotificationController,
            ParamController,
            PatchController,
            PluginsController
        ]
        if test:
            from unittest.mock import Mock 
            controllers.remove(DeviceController)
            self.controllers[DeviceController.__name__] = Mock(spec=DeviceController)

        for controller in controllers:
            self.controllers[controller.__name__] = controller(self)

        for controller in list(self.controllers.values()):
            controller.configure()

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
