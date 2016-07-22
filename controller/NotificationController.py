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
    def notifyCurrentPatchChange(self, patch):
        for observer in self.observers:
            observer.onCurrentPatchChange(patch)

    def notifyBankUpdate(self, bank, updateType):
        for observer in self.observers:
            observer.onBankUpdate(bank, updateType)

    def notifyPatchUpdated(self, patch, updateType):
        for observer in self.observers:
            observer.onPatchUpdated(patch, updateType)
            
    def notifyEffectUpdated(self, effect, updateType):
        for observer in self.observers:
            observer.onEffectUpdated(effect, updateType)

    def notifyEffectStatusToggled(self, effect):
        for observer in self.observers:
            observer.onEffectStatusToggled(effect)

    def notifyParamValueChange(self, param):
        for observer in self.observers:
            observer.onParamValueChange(param)
