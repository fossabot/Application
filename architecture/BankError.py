# -*- coding: utf-8 -*-


class BankError(Exception):

    def __init__(self, message):
        super(BankError, self).__init__(message)
        self.message = message
