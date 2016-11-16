import time

from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController
from application.controller.component_data_controller import ComponentDataController
from application.controller.device_controller import DeviceController
from application.controller.effect_controller import EffectController
from application.controller.notification_controller import NotificationController
from application.controller.param_controller import ParamController
from application.controller.patch_controller import PatchController
from application.controller.plugins_controller import PluginsController


class Application(object):
    """
    Application is a API for pythonic management with LV2 audio plugins.
    Current, it offers a bridge with `mod-host`_
    (LV2 host for Jack controllable via socket or command line)
    by a *TCP* connection.

    By a application instance, it's possible obtains a :class:Controller
    for control::

        >>> from Application import Application
        >>> from controller.CurrentController import CurrentController

        >>> application = Application()
        >>> current_controller = application.controller(CurrentController)

        >>> print(current_controller.current_patch)
        <Patch object as Shows with 2 effects at 0x7fa3bcb49be0>

        >>> current_controller.to_next_patch()
        >>> current_controller.current_patch
        <Patch object as Shows 2 with 1 effects at 0x7fa3bbcdecf8>

    For more details, please, see the Controllers extended classes.

    :param string data_patch: Uri where the data will be persisted
    :param string address: `mod-host`_ address
    :param bool test: If ``test == True``, the connection with mod-host will be simulated

    .. _mod-host: https://github.com/moddevices/mod-host
    """

    def __init__(self, data_patch="data/", address="localhost", test=False):
        self.dataPatch = data_patch
        self.components = []
        self.controllers = self._load_controllers(address, test)

        self._configure_controllers(self.controllers)

    def _load_controllers(self, address, test):
        controllers = {}

        list_controllers = [
            BanksController,
            ComponentDataController,
            CurrentController,
            EffectController,
            NotificationController,
            ParamController,
            PatchController,
            PluginsController
        ]

        controllers[DeviceController.__name__] = self._init_device_controller(address, test)

        for controller in list_controllers:
            controllers[controller.__name__] = controller(self)

        return controllers

    def _init_device_controller(self, address, test):
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

    def controller(self, controller):
        """
        Returns the controller instance by Controller class identifier

        :param Controller controller: Class identifier
        :return: Controller instance
        """
        return self.controllers[controller.__name__]

    def dao(self, dao):
        """
        Returns a Dao persister instance by Dao class identifier

        :param dao: Class identifier
        :return: Dao instance
        """
        return dao(self.dataPatch)
