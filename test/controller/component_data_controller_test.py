from application.controller.component_data_controller import ComponentDataController

from test.controller.controller_test import ControllerTest


'''
class ComponentDataControllerTest(ControllerTest):
    application = None
    controller = None
    banksController = None
    key = None

    def setUp(self):
        self.key = 'ComponentDataControllerTest'
        self.controller = self.get_controller(ComponentDataController)

    def get_controller(self, controller):
        return ComponentDataControllerTest.application.controller(controller)

    def test_empty_get(self):
        self.assertEqual(self.controller[self.key], {})

    def test_content_get(self):
        data = {'test': 'test_content_get'}

        self.controller[self.key] = data
        self.assertEqual(self.controller[self.key], data)

        del self.controller[self.key]

    def test_override_content(self):
        data = {'test': 'test_override_content'}
        data2 = {'test': 'test_override_content', 'fu': 'bá'}

        self.controller[self.key] = data
        self.assertEqual(self.controller[self.key], data)
        self.controller[self.key] = data2
        self.assertEqual(self.controller[self.key], data2)

        del self.controller[self.key]

    def test_directly_changes_not_works(self):
        self.controller[self.key] = {'test': 'test_directly_changes_not_works'}

        data = self.controller[self.key]
        data['new-key'] = 'new value'

        self.assertNotEqual(self.controller[self.key], data)

        del self.controller[self.key]

    def test_delete_content(self):
        data = {'test': 'test_delete_content'}

        self.controller[self.key] = data
        self.assertNotEqual(self.controller[self.key], {})
        del self.controller[self.key]

        self.assertEqual(self.controller[self.key], {})
'''
