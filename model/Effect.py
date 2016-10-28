# -*- coding: utf-8 -*-
from model.Param import Param


class Effect(object):
    """
    Representation of a audio plugin.

    Effect contains a status (off=bypass) and a list of :class:`Param`

    :param dict json: Json representation of Bank
    :param Patch patch: Effect :class:`Patch`
    """

    def __init__(self, json, patch=None):
        self.__json = json
        self.patch = patch

    @property
    def json(self):
        """
        Get a json representation of this effect

        :return dict: json representation
        """
        return self.__json

    @json.setter
    def json(self, value):
        """
        Change this effect by a json representation

        .. note::
            Caution, please

        .. warning::
           This implementation set the original json (passed in constructor).
           for reflects changes in patch

        :param dict value: Json representation
        """
        self.__json.clear()
        self.__json.update(value)

    def __eq__(self, another):
        """
        Compare if this effect is equals with another effect

        :param Effect another: Other effect that be comparable
        :return bool: This effect is equals to another effect?
        """
        return isinstance(another, self.__class__) \
           and self.json == another.json

    def __ne__(self, another):
        """
        Compare if this effect are not equals with another effect

        :param Effect another: Other effect that be comparable
        :return bool: This effect is not equals to another effect?
        """
        return not self.__eq__(another)

    def __getitem__(self, key):
        return self.json[key]

    @property
    def index(self):
        """
        :return int: Effect index
        """
        return self.patch.indexOfEffect(self)

    @property
    def params(self):
        """
        Returns all :class:`Param` of this effect
        """
        returned = []

        for param in self["ports"]["control"]["input"]:
            returned.append(Param(param, self))

        return returned

    @property
    def status(self):
        """
        Returns the effect status. When ``False==bypass``

        :return bool: Effect status.
        """
        return self['status']

    def indexOfParam(self, param):
        """
        .. note::
            Use :func:`index` :class:`Param` attribute instead.

        :param Param param:
        :return: Index of the param
        """
        return self["ports"]["control"]["input"].index(param.json)
