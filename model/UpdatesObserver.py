# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from enum import Enum


class UpdateType(Enum):
    """
    Enumeration for informs the change type
    """
    CREATED = 0
    UPDATED = 1
    DELETED = 2


class UpdatesObserver(metaclass=ABCMeta):
    """
    :class:`NotificationObserver` notifies all :class:`UpdatesObserver`
    registered then occurs any change in Bank, Patch, Effect, etc.

    The :class:`UpdatesObserver` methods are called when your respective
    change occurs if your ``token`` are different of the requisitor token
    """
    def __init__(self):
        self._token = None

    @property
    def token(self):
        """
        :return string: Observer token
        """
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @abstractmethod
    def onCurrentPatchChange(self, patch, token=None):
        """
        Called when the current patch changes

        :param Patch patch: New current patch
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def onBankUpdate(self, bank, update_type, token=None):
        """
        Called when changes occurs in any :class:`Bank`

        :param Bank patch: Bank changed.
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def onPatchUpdated(self, patch, update_type, token=None):
        """
        Called when changes occurs in any :class:`Patch`

        :param Patch patch: Patch changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def onEffectUpdated(self, effect, update_type, token=None):
        """
        Called when changes occurs in any :class:`Effect`

        :param Effect effect: Effect changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def onEffectStatusToggled(self, effect, token=None):
        """
        Called when any :class:`Effect` status is toggled

        :param Effect effect: Effect when status has been toggled
        :param string token: Request token identifier
        """
        pass

    @abstractmethod
    def onParamValueChange(self, param, token=None):
        """
        Called when a param value change

        :param Param param: Param with value changed
        :param string token: Request token identifier
        """
        pass
