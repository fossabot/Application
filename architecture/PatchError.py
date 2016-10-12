# -*- coding: utf-8 -*-


class PatchError(Exception):

    def __init__(self, message):
        super(PatchError, self).__init__(message)
        self.message = message
