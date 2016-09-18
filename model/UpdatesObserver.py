# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from enum import Enum


class UpdateType(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2


class UpdatesObserver(metaclass=ABCMeta):

    @abstractmethod
    def onCurrentPatchChange(self, patch, token=None):
        pass

    @abstractmethod
    def onBankUpdate(self, bank, update_type, token=None):
        pass

    @abstractmethod
    def onPatchUpdated(self, patch, update_type, token=None):
        pass

    @abstractmethod
    def onEffectUpdated(self, effect, update_type, token=None):
        pass

    @abstractmethod
    def onEffectStatusToggled(self, effect, token=None):
        pass

    @abstractmethod
    def onParamValueChange(self, param, token=None):
        pass
