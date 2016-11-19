from application.controller.effect_controller import EffectController
from application.controller.notification_controller import NotificationController
from application.controller.param_controller import ParamController
from application.controller.plugins_controller import PluginsController

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.patch import Patch

from test.controller.controller_test import ControllerTest

from unittest.mock import MagicMock


class ParamControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'PARAM_TOKEN'

        controller = ParamControllerTest.application.controller
        self.controller = controller(ParamController)
        self.effect_controller = controller(EffectController)
        self.notifier = controller(NotificationController)

        self.plugins = controller(PluginsController)

    def test_update_value(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_effect Bank')
        patch = Patch('test_create_effect Patch')
        bank.append(patch)
        reverb = self.plugins.lv2_effect('http://calf.sourceforge.net/plugins/Reverb')
        patch.append(reverb)

        param = reverb.params[0]

        param.value = param.minimum
        self.controller.updated_value(param)
        observer.on_param_value_changed.assert_called_with(param, None)

        param.value = param.maximum
        self.controller.updated_value(param, self.TOKEN)
        observer.on_param_value_changed.assert_called_with(param, self.TOKEN)
