# -*- coding: utf-8 -*-


class Banks(object):
    """
    Banks group all persisted :class:`Bank`
    """

    def __init__(self):
        self.index = 0
        self.banks = {}

    @property
    def json(self):
        """
        Get a json representation of all banks

        :return dict: Json representation
        """
        banks = []
        for bank in self.all:
            banks.append(bank.json)

        return banks

    @property
    def all(self):
        """
        Returns all banks ordered by your id

        :return list[Bank]: The banks of this instance contains
        """
        return sorted(list(self.banks.values()), key=lambda bank: bank.index)

    def __len__(self):
        """
        :return int: Returns total of banks of this instance
        """
        return len(self.banks)

    def __getitem__(self, index):
        """
        Get :class:`Bank` by index

        :param int index: Bank index
        :return Bank: Bank with index transferred
        """
        try:
            return self.banks[index]
        except KeyError:
            raise IndexError("Bank not found")

    def __delitem__(self, index):
        """
        Remove :class:`Bank` by index

        :param int index: Bank index
        """
        try:
            del self.banks[index]
        except KeyError:
            raise IndexError("Bank not found")

    def append(self, bank):
        """
        Add a :class:`Bank` in this

        :param Bank bank: Bank that will be added
        """
        if bank.index == -1:
            bank.index = self.index
            self.index = bank.index + 1

        elif bank.index >= self.index:
            self.index = bank.index + 1

        self.banks[bank.index] = bank

    def swap(self, bankA, bankB):
        """
        .. deprecated:: ever
            Don't use
        """
        bankA.index, bankB.index = bankB.index, bankA.index

        self.banks[bankA.index] = bankA
        self.banks[bankB.index] = bankB