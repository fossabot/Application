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

from test.controller.controller_test import ControllerTest

from application.controller.current_controller import CurrentController
from application.component.component import Component

from unittest.mock import MagicMock


class ComponentExample(Component):
    def init(self):
        pass


class ComponentTest(ControllerTest):

    def test_register(self):
        app = ComponentTest.application

        component = ComponentExample(app)
        app.register(component)

        self.assertEqual(app.components[0], component)

        del app.components[0]

    def test_controller(self):
        app = ComponentTest.application

        component = ComponentExample(app)
        app.register(component)

        self.assertEqual(app.controller(CurrentController), component.controller(CurrentController))

        del app.components[0]

    def test_register_observer(self):
        app = ComponentTest.application

        component = ComponentExample(app)
        app.register(component)

        mock = MagicMock()
        component.register_observer(mock)

        self.assertEqual(app.components_observer.observers[0], mock)

        component.unregister_observer(mock)

        self.assertEqual(len(app.components_observer.observers), 0)
        del app.components[0]
