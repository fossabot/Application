from architecture.EffectException import EffectException

from controller.EffectController import EffectController
from controller.PluginsController import PluginsController
from controller.CurrentController import CurrentController

from test.controller.controller_test import ControllerTest

'''
class EffectControllerTest(ControllerTest):
    application = None
    controller = None

    plugins_controller = None
    current_controller = None
    current_bank = None
    current_patch = None

    def setUp(self):
        self.controller = self._get_controller(EffectController)
        self.plugins_controller = self._get_controller(PluginsController)
        self.current_controller = self._get_controller(CurrentController)

        self.current_controller.setBank(0)
        self.current_controller.setPatch(0)

        self.current_bank = self.current_controller.currentBank
        self.current_patch = self.current_controller.currentPatch

    def _get_controller(self, controller):
        return EffectControllerTest.application.controller(controller)

    def _total_effects_current_patch(self):
        return len(self.current_patch['effects'])

    def _any_plugin_uri(self):
        return list(self.plugins_controller.plugins.keys())[0]

    def _create_effect(self, uri=None, patch=None):
        if uri is None:
            uri = self._any_plugin_uri()

        patch = self.current_patch if patch is None else patch
        return self.controller.createEffect(patch, uri)

    def test_create_effect(self):
        total_effects = self._total_effects_current_patch()

        effect_index = self._create_effect()
        effect = self.current_patch.effects[effect_index]

        # Index is last effect + 1
        self.assertEqual(total_effects, effect_index)

        self.assertLess(total_effects, self._total_effects_current_patch())

        self.controller.deleteEffect(effect)

    def test_create_undefined_effect(self):
        with self.assertRaises(EffectException):
            self._create_effect('http://undefined.plugin.uri')

    def test_delete_effect(self):
        effect_index = self._create_effect()
        effect = self.current_patch.effects[effect_index]

        total_effects = self._total_effects_current_patch()

        self.controller.deleteEffect(effect)

        self.assertEqual(total_effects - 1, self._total_effects_current_patch())

    def test_delete_undefined_effect(self):
        effect_index = self._create_effect()
        effect = self.current_patch.effects[effect_index]

        self.controller.deleteEffect(effect)

        with self.assertRaises(EffectException):
            self.controller.deleteEffect(effect)

    def test_connect_effects(self):
        effect_index_a = self._create_effect(uri='http://guitarix.sourceforge.net/plugins/gx_tremolo#_tremolo')
        effect_a = self.current_patch.effects[effect_index_a]

        effect_index_b = self._create_effect(uri='http://guitarix.sourceforge.net/plugins/gxts9#ts9sim')
        effect_b = self.current_patch.effects[effect_index_b]

        total_connections = len(self.current_patch.connections)
        self.controller.connect(effect_a, effect_a.outputs[0], effect_b, effect_b.inputs[0])

        self.assertEqual(total_connections+1, len(self.current_patch.connections))

        self.controller.deleteEffect(effect_a)
        self.controller.deleteEffect(effect_b)

    def test_connect_effects_different_patch(self):
        effect_a_uri = 'http://guitarix.sourceforge.net/plugins/gx_tremolo#_tremolo'
        effect_index_a = self._create_effect(uri=effect_a_uri, patch=self.current_controller.currentPatch)
        effect_a = self.current_controller.currentPatch.effects[effect_index_a]

        self.current_controller.toNextPatch()

        effect_b_uri = 'http://guitarix.sourceforge.net/plugins/gxts9#ts9sim'
        effect_b_index = self._create_effect(uri=effect_b_uri, patch=self.current_controller.currentPatch)
        effect_b = self.current_controller.currentPatch.effects[effect_b_index]

        self.current_controller.toBeforePatch()

        with self.assertRaises(EffectException):
            self.controller.connect(effect_a, effect_a.outputs[0], effect_b, effect_b.inputs[0])

        self.controller.deleteEffect(effect_a)
        self.controller.deleteEffect(effect_b)

    def test_delete_effect_remove_connections(self):
        effect_index_a = self._create_effect(uri='http://guitarix.sourceforge.net/plugins/gx_tremolo#_tremolo')
        effect_a = self.current_patch.effects[effect_index_a]

        effect_index_b = self._create_effect(uri='http://guitarix.sourceforge.net/plugins/gxts9#ts9sim')
        effect_b = self.current_patch.effects[effect_index_b]

        original_total_connections = len(self.current_patch.connections)

        self.controller.connect(effect_a, effect_a.outputs[0], effect_b, effect_b.inputs[0])
        self.assertEqual(original_total_connections+1, len(self.current_patch.connections))

        self.controller.deleteEffect(effect_a)
        self.controller.deleteEffect(effect_b)

        self.assertEqual(original_total_connections, len(self.current_patch.connections))
'''
