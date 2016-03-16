from controller.BanksController import BanksController
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.PluginsController import PluginsController


class Application:
    controllers = {}
    
    def __init__(self):
        controllers = [BanksController, CurrentController, DeviceController, PluginsController]
        
        for controller in controllers:
            self.controllers[controller] = controller(self)
            
        for controller in self.controllers.values():
            controller.configure()
        
    def dao(self, dao):
        DATA_PATH = "data/"
        
        return dao(DATA_PATH)
    
    def controller(self, controller):
        return self.controllers[controller]