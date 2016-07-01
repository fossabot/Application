# -*- coding: utf-8 -*-
from controller.Controller import Controller


class NotificationController(Controller):
    """
    Notification observer notifies changes to 
    UpdatesObservers registred
    """
    observers = []

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    ########################
    # Notify methods
    ########################
    def notifyCurrentBankChange(self, bankIndex):
        for observer in self.observers:
            observer.onCurrentBankChange(bankIndex)

    def notifyCurrentPatchChange(self, patchIndex):
        for observer in self.observers:
            observer.onCurrentPatchChange(patchIndex)

    def notifyBankUpdate(self, bankIndex):
        for observer in self.observers:
            observer.onBankUpdate(bankIndex)

    def notifyPatchUpdate(self, bankIndex, patch):
        for observer in self.observers:
            observer.onPatchUpdate(bankIndex, patch)

    def notifyParamValueChange(self, bankIndex, patchIndex, effect, param):
        for observer in self.observers:
            observer.onParamValueChange(bankIndex, patchIndex, effect, param)
