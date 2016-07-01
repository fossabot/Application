# -*- coding: utf-8 -*-
from controller.Controller import Controller


class NotificationController(Controller):
    """
    Notification observer notifies changes to 
    UpdatesObservers registred
    """
    observers = []

    def configure(self):
        pass

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    ########################
    # Notify methods
    ########################
    def notifyCurrentPatchChange(self, bankIndex, patchIndex):
        for observer in self.observers:
            observer.onCurrentPatchChange(bankIndex, patchIndex)

    def notifyBankUpdate(self, bankIndex):
        for observer in self.observers:
            observer.onBankUpdate(bankIndex)

    def notifyPatchUpdate(self, bankIndex, patchIndex):
        for observer in self.observers:
            observer.onPatchUpdate(bankIndex, patchIndex)

    def notifyParamValueChange(self, bankIndex, patchIndex, effectIndex, param):
        for observer in self.observers:
            observer.onParamValueChange(bankIndex, patchIndex, effectIndex, param)
