# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class UpdatesObserver(metaclass=ABCMeta):

    @abstractmethod
    def onCurrentPatchChange(self, bankIndex, patchIndex):
        pass

    @abstractmethod
    def onBankUpdate(self, bankIndex):
        pass

    @abstractmethod
    def onPatchUpdate(self, bankIndex, patchIndex):
        pass

    @abstractmethod
    def onParamValueChange(self, bankIndex, patchIndex, effectIndex, paramIndex):
        pass
