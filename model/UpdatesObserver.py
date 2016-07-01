# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from enum import Enum


class UpdateType(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2


class UpdatesObserver(metaclass=ABCMeta):

    @abstractmethod
    def onCurrentPatchChange(self, bankIndex, patchIndex):
        pass

    @abstractmethod
    def onBankUpdate(self, bankIndex, updateType):
        pass

    @abstractmethod
    def onPatchUpdate(self, bankIndex, patchIndex, updateType):
        pass

    @abstractmethod
    def onParamValueChange(self, bankIndex, patchIndex, effectIndex, paramIndex, updateType):
        pass
