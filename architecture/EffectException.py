# -*- coding: utf-8 -*-


class EffectException(Exception):

    def __init__(self, message):
        super(EffectException, self).__init__(message)
        self.message = message
