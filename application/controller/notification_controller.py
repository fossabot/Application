# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from application.controller.controller import Controller


class NotificationController(Controller):
    """
    Notifies request changes to all :class:`ApplicationObserver` registered
    than not contains the same request *token*.
    """

    def __init__(self, app):
        super().__init__(app)

    def configure(self):
        pass

    def is_requester(self, observer, token):
        """
        Verify if the observer is the requester change (if observer contains
        same token that token informed)

        :param ApplicationObserver observer:
        :param string token: Request token identifier
        :return: The requisition is realized by observer?
        """
        return observer.token is not None and observer.token == token

    ########################
    # Notify methods
    ########################
    def current_pedalboard_changed(self, pedalboard, token=None):
        """
        Notify **current pedalboard** change.

        :param Pedalboard pedalboard: New current pedalboard
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_current_pedalboard_changed(pedalboard, token)
