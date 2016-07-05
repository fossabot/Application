# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from enum import Enum


class UpdateType(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2


class UpdatesObserver(metaclass=ABCMeta):

    @abstractmethod
    def onCurrentPatchChange(self, patch):
        pass

    @abstractmethod
    def onBankUpdate(self, bank, updateType):
        pass

    @abstractmethod
    def onPatchUpdated(self, patch, updateType):
        pass

    @abstractmethod
    def onEffectUpdated(self, effect, updateType):
        pass

    @abstractmethod
    def onEffectStatusToggled(self, effect):
        pass

    @abstractmethod
    def onParamValueChange(self, param):
        pass
