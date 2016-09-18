# -*- coding: utf-8 -*-
from controller.Controller import Controller


class NotificationController(Controller):
    """
    Notification observer notifies changes to
    UpdatesObservers registered
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
    def notifyCurrentPatchChange(self, patch, token=None):
        for observer in self.observers:
            observer.onCurrentPatchChange(patch, token)

    def notifyBankUpdate(self, bank, update_type, token=None):
        for observer in self.observers:
            observer.onBankUpdate(bank, update_type, token)

    def notifyPatchUpdated(self, patch, update_type, token=None):
        for observer in self.observers:
            observer.onPatchUpdated(patch, update_type, token)
            
    def notifyEffectUpdated(self, effect, update_type, token=None):
        for observer in self.observers:
            observer.onEffectUpdated(effect, update_type, token)

    def notifyEffectStatusToggled(self, effect, token=None):
        for observer in self.observers:
            observer.onEffectStatusToggled(effect, token)

    def notifyParamValueChange(self, param, token=None):
        for observer in self.observers:
            observer.onParamValueChange(param, token)
