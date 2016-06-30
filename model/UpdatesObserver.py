# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class UpdatesObserver(metaclass=ABCMeta):

    @abstractmethod
    def onCurrentBankChange(self, bankIndex):
        pass

    @abstractmethod
    def onCurrentPatchChange(self, patchIndex):
        pass

    @abstractmethod
    def onBankUpdate(self, bankIndex):
        pass

    @abstractmethod
    def onPatchUpdate(self, bankIndex, patch):
        pass

    @abstractmethod
    def onParamValueChange(self, bankIndex, patchIndex, effect, param):
        pass
