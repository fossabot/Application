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

from application.controller.notification_controller import NotificationController
from application.controller.param_controller import ParamController
from application.controller.plugins_controller import PluginsController

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard

from test.controller.controller_test import ControllerTest

from unittest.mock import MagicMock


class ParamControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'PARAM_TOKEN'

        controller = ParamControllerTest.application.controller
        self.controller = controller(ParamController)
        self.notifier = controller(NotificationController)

        self.plugins = controller(PluginsController)

    def test_updated_value(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_value Bank')
        pedalboard = Pedalboard('test_update_value Pedalboard')
        bank.append(pedalboard)
        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')
        pedalboard.append(reverb)

        param = reverb.params[0]

        param.value = param.minimum
        self.controller.updated(param)
        observer.on_param_value_changed.assert_called_with(param, None)

        param.value = param.maximum
        self.controller.updated(param, self.TOKEN)
        observer.on_param_value_changed.assert_called_with(param, self.TOKEN)

        self.notifier.unregister(observer)
