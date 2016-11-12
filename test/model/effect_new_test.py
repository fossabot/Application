import unittest
from unittest.mock import MagicMock

from model.lv2.lv2_effect_builder import Lv2EffectBuilder


class EffectTest(unittest.TestCase):

    def test_active(self):
        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        reverb.observer = MagicMock()

        self.assertEqual(True, reverb.active)
        reverb.active = False
        reverb.observer.onEffectStatusToggled.assert_called_with(reverb)
        self.assertEqual(False, reverb.active)

    def test_active_same_state(self):
        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        reverb.observer = MagicMock()

        self.assertEqual(True, reverb.active)
        reverb.active = True
        reverb.observer.onEffectStatusToggled.assert_not_called()

    def test_toggle(self):
        builder = Lv2EffectBuilder()
        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        reverb.observer = MagicMock()

        self.assertEqual(True, reverb.active)
        reverb.toggle()
        reverb.observer.onEffectStatusToggled.assert_called_with(reverb)
        self.assertEqual(False, reverb.active)

