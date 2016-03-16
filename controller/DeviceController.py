from controller.Controller import Controller

'''
Changes in the device
'''
class DeviceController(Controller):
    
    def setPatch(self, patch):
        print("Loading effects", patch["effects"])
        print("connecting", patch["connections"])

    def toggleStatusEffect(self, effect):
        print("Toggle status effect number:", effect)
        
    def setEffectParam(self, effect, param):
        print("Toggle status effect number:", effect)