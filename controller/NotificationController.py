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
