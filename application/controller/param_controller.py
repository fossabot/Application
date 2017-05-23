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
from application.controller.notification_controller import NotificationController


class ParamController(Controller):
    """
    Notify all observers that a :class:`.Param` has been updating your value
    """

    def __init__(self, application):
        super(ParamController, self).__init__(application)
        self.notifier = None

    def configure(self):
        self.notifier = self.app.controller(NotificationController)

    def updated(self, param, token=None):
        """
        Notify all observers that a new :class:`.Param` object has been updated.

        .. note::

            Change the param value before to notify

            >>> param.value = new_value
            >>> param_controller.updated(param)

        :param Param param: Effect parameter with your value changed
        :param string token: Request token identifier
        """
        self.notifier.param_value_changed(param, token)
