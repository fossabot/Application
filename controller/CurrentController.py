from architecture.privatemethod import privatemethod

from controller.Controller import Controller
from controller.BanksController import BanksController
from controller.PluginsController import PluginsController
from controller.DeviceController import DeviceController

from dao.CurrentDao import CurrentDao

class CurrentController(Controller):
    bank = 0
    patch = 0

    def configure(self):
        data = self.app.dao(CurrentDao).load()
        self.bank = data["bank"]
        self.patch = data["patch"]
        
        self.deviceController = self.app.controller(DeviceController)

    '''
    ************************
    Effect
    ************************
    '''
    def toggleStatusEffect(self, effectNumber):
        effect = self.getEffect(effectNumber)
        effect["active"] = not effect["active"]

        self.deviceController.toggleStatusEffect(effectNumber)
        self.saveCurrent()
    
    def setEffectParam(self, effectNumber, param):
        effect = self.getEffect(effectNumber)

        self.deviceController.setEffectParam(effectNumber)
        self.saveCurrent()

    @privatemethod
    def getEffect(self, effectNumber):
        patch = self.getCurrentPatch()
        try:
            return patch["effects"][effectNumber]
        except IndexError:
            raise IndexError("Element not found")
        
    '''
    ************************
    Current Patch/Bank
    ************************
    '''
    def setPatch(self, patch):
        if self.patch == patch:
            return
        self.setCurrent(self.bank, patch)

    def setBank(self, bank):
        if self.bank == bank:
            return
        self.setCurrent(bank, 0)

    @privatemethod
    def setCurrent(self, bank, patch):
        self.loadDevicePatch(bank, patch) #throwable. need be first
        self.bank = bank
        self.patch = patch
        self.saveCurrent()
        
    @privatemethod
    def saveCurrent(self):
        print("saving:", self.bank)

    @privatemethod
    def loadDevicePatch(self, bank, patch):
        patch = self.getPatch(bank, patch)
        self.deviceController.setPatch(patch)
    
    @privatemethod
    def getCurrentPatch(self):
        return self.getPatch(self.bank, self.patch)
    
    @privatemethod
    def getPatch(self, bank, patch):
        banksController = self.app.controller(BanksController)
        
        bank = banksController.banks[bank]
        return bank.getPatch(patch)