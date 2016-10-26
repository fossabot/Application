# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    """
    Abstract class for Application controllers.

    Extends to offer functionalities for this API. Remember to manually register
    the extended class in :class:`Application` (in private ``_load_controllers``
    method)

    :param Application application: :class:`Application` instance
    """
    def __init__(self, application):
        self.app = application

    @abstractmethod
    def configure(self):
        """
        Configure is called by :class:`Application` for initialize this object
        """
        raise NotImplementedError()
