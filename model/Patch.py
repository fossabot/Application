# -*- coding: utf-8 -*-
from model.Effect import Effect
from architecture.PatchError import PatchError


class Patch(object):
    """
    :class:`Patch` contains a list of :class:`Effect`.

    .. note::
       In the future, will be contains the connections
       between effects too.

    :param dict json: Json representation of :class:`Patch`
    :param Bank bank: Patch :class:`Bank`
    """

    def __init__(self, json, bank=None):
        self.bank = bank
        self.__json = json  # Reference is important, don't use dict(json)

    @property
    def json(self):
        """
        Get a json representation of this patch

        :return dict: json representation
        """
        return self.__json
    
    @json.setter
    def json(self, value):
        """
        Change this patch by a json representation

        .. note::
            Caution, please

        .. warning::
           This implementation set the original json (passed in constructor).
           for reflects changes in bank

        :param dict value: Json representation
        """
        self.__json.clear()
        self.__json.update(value)

    def __getitem__(self, key):
        """
        :param string key: Property key
        :return: Returns a Patch property
        """
        return self.json[key]

    def __eq__(self, another):
        """
        Compare if this patch is equals with another patch

        :param Patch another: Other patch that be comparable
        :return bool: This patch is equals to another patch?
        """
        return isinstance(another, self.__class__) \
           and self.json == another.json

    def __ne__(self, another):
        """
        Compare if this patch are not equals with another patch

        :param Patch another: Other patch that be comparable
        :return bool: This patch is not equals to another patch?
        """
        return not self.__eq__(another)

    @property
    def effects(self):
        """
        Returns all :class:`Effects` of this bank
        """
        returned = []
        effects = self.json["effects"]

        for effectJson in effects:
            returned.append(Effect(effectJson, self))

        return returned

    @property
    def index(self):
        """
        :return int: Patch index
        """
        return self.bank.indexOfPatch(self)

    def addEffect(self, effect):
        """
        Add a :class:`Effect` in this patch

        :param Effect effect: Effect that will be added
        """
        self["effects"].append(effect.json)
        effect.patch = self

    def indexOfEffect(self, effect):
        """
        .. note::
            Use :func:`index` :class:`Effect` attribute instead.

        :param Effect effect:
        :return: Index of the effect
        """
        return self["effects"].index(effect.json)

    def swapEffects(self, effectA, effectB):
        """
        .. deprecated:: ever
           Don't use
        """
        if effectA.patch != self or effectB.patch != self:
            raise PatchError("effectA or effectB aren't in this patch")

        indexA = effectA.index
        indexB = effectB.index

        effects = self.json['effects']

        effects[indexA], effects[indexB] = effects[indexB], effects[indexA]

    def __repr__(self, *args, **kargs):
        return "<%s object as %s with %d effects at 0x%x>" % (
            self.__class__.__name__,
            self["name"],
            len(self.effects),
            id(self)
        )
