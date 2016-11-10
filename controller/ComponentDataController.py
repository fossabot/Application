# -*- coding: utf-8 -*-
from dao.ComponentDao import ComponentDao

from controller.Controller import Controller


class ComponentDataController(Controller):
    """
    Maybe the patch data it's not sufficient for management in a custom
    :class:`Components`. For example, in a possible visual patch manager is
    necessary persist the effects positions.

    :class:`ComponentDataController` offers a way to salve and restore data.

    For your component, create a unique identifier (key) and use it for manage all
    your Component data. For example::

        >>> key = 'raspberry-p0'
        >>> controller = application.controller(ComponentDataController)

        >>> # If key not exists, returns {}
        >>> controller[key]
        {}

        >>> controller[key] = {'patch': 0}
        >>> controller[key]
        {'patch': 0}

        >>> # The new data overrides old data
        >>> controller[key] = {'patches': []}
        >>> controller[key]
        {'patches': []}

        >>> # Changes in returned object will not change the persisted data
        >>> data = controller[key]
        >>> data['component'] = 'Raspberry P0'
        >>> data
        {'patches': [], 'component': 'Raspberry P0'}
        >>> controller[key]
        {'patches': []}

        >>> # Remove all content for 'raspberry-p0'
        >>> del controller[key]
        >>> controller[key]
        {}

    .. warning::
        :class:`ComponentDataController` does not have access control,
        which means that any Component that eventually
        use *ComponentDataController* may interfere with the content
        (accessing, changing or removing).

    .. warning::
        It's a easy way for save simple data. Please, don't save binaries or big content
    """

    dao = None
    __data = None

    def configure(self):
        self.dao = self.app.dao(ComponentDao)
        self.__data = self.dao.load()

    def __getitem__(self, key):
        """
        Returns the data for the informed `key`

        :param string key:
        :return dict: Content if exist for key informed, else empty `dict`
        """
        try:
            return dict(self.__data[key])
        except KeyError:
            return {}

    def __setitem__(self, key, value):
        """
        Change the `key` identifier content to `value`

        :param string key: Identifier
        :param value: Data will be persisted
        """
        self.__data[key] = value

        self.dao.save(self.__data)

    def __delitem__(self, key):
        """
        Remove all `item` identifier content

        :param string key: Identifier
        """
        del self.__data[key]

        self.dao.save(self.__data)
