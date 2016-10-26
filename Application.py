import time

from controller.BanksController import BanksController
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.EffectController import EffectController
from controller.NotificationController import NotificationController
from controller.ParamController import ParamController
from controller.PatchController import PatchController
from controller.PluginsController import PluginsController


class Application(object):

    def __init__(self, data_patch="data/", address="localhost", test=False):
        self.dataPatch = data_patch
        self.controllers = self._load_controllers(address, test)
        self._configure_controllers(self.controllers)
        self.components = []

    def _load_controllers(self, address, test):
        controllers = {}

        list_controllers = [
            BanksController,
            CurrentController,
            EffectController,
            NotificationController,
            ParamController,
            PatchController,
            PluginsController
        ]

        controllers[DeviceController.__name__] = self.init_device_controller(address, test)

        for controller in list_controllers:
            controllers[controller.__name__] = controller(self)

        return controllers

    def init_device_controller(self, address, test):
        if test:
            from unittest.mock import Mock
            return Mock(spec=DeviceController)

        else:
            device_controller = DeviceController(self)
            device_controller.address = address

            return device_controller

    def _configure_controllers(self, controllers):
        for controller in list(controllers.values()):
            controller.configure()

    def dao(self, dao):
        return dao(self.dataPatch)

    def controller(self, controller):
        return self.controllers[controller.__name__]

    def register(self, component):
        """
        Register a :class:`Component` extended class into Application.
        The components will be loaded when application is loaded (after `start` method is called).

        :param Component component: A module to be loaded when the Application is loaded
        """
        self.components.append(component)

    def start(self):
        """
        Start this API, initializing the components.
        """
        for component in self.components:
            print('[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']', 'Loading', component.__class__.__name__)
            component.init()


class ApplicationSingleton(object):
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Application(test=True)

        return cls.instance
