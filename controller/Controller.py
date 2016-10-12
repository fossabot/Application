# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def configure(self):
        pass
