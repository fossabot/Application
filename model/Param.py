# -*- coding: utf-8 -*-


class Param(object):
    """
    :class:`Param` is an object representation of an Audio Plugin
    Parameter

    :param dict json: Json representation of Param
    :param Effect effect: Param :class:`Effect`
    """

    def __init__(self, json, effect=None):
        self.__json = json
        self.effect = effect

    @property
    def json(self):
        """
        Get a json representation of this param

        :return dict: json representation
        """
        return self.__json

    def __eq__(self, another):
        """
        Compare if this param is equals with another param

        :param Param another: Other param that be comparable
        :return bool: This param is equals to another param?
        """
        return isinstance(another, self.__class__) \
           and self.json == another.json

    def __ne__(self, another):
        """
        Compare if this param are not equals with another param

        :param Param another: Other param that be comparable
        :return bool: This param is not equals to another param?
        """
        return not self.__eq__(another)

    def __getitem__(self, key):
        """
        :param string key: Property key
        :return: Returns a Effect property
        """
        return self.json[key]

    @property
    def value(self):
        """
        :return: Returns the param value
        """
        return self["value"]

    @value.setter
    def value(self, value):
        """
        Set the param value

        :param value: New param value
        """
        self.__json["value"] = value

    @property
    def index(self):
        """
        :return int: Param
        """
        return self.effect.indexOfParam(self)
