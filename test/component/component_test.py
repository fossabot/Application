from test.controller.controller_test import ControllerTest

from application.controller.notification_controller import NotificationController
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

        self.assertEqual(app.controller(NotificationController), component.controller(NotificationController))

        del app.components[0]

    def test_register_observer(self):
        app = ComponentTest.application

        component = ComponentExample(app)
        app.register(component)

        mock = MagicMock()
        component.register_observer(mock)

        self.assertEqual(app.controller(NotificationController).observers[0], mock)

        component.unregister_observer(mock)

        self.assertEqual(len(app.controller(NotificationController).observers), 0)
        del app.components[0]
