from unittest.mock import MagicMock
from application.component.application_observer import ApplicationObserver


class MockObserver(ApplicationObserver):

    def __init__(self):
        super().__init__()
        self.on_current_pedalboard_changed = MagicMock()
        self.on_bank_updated = MagicMock()
        self.on_pedalboard_updated = MagicMock()
        self.on_effect_updated = MagicMock()
        self.on_effect_status_toggled = MagicMock()
        self.on_param_value_changed = MagicMock()
        self.on_connection_updated = MagicMock()

    def reset_mock(self):
        self.on_current_pedalboard_changed.reset_mock()
        self.on_bank_updated.reset_mock()
        self.on_pedalboard_updated.reset_mock()
        self.on_effect_updated.reset_mock()
        self.on_effect_status_toggled.reset_mock()
        self.on_param_value_changed.reset_mock()
        self.on_connection_updated.reset_mock()

    def on_current_pedalboard_changed(self, pedalboard, **kwargs):
        pass

    def on_bank_updated(self, bank, update_type, index, origin, **kwargs):
        pass

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        pass

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        pass

    def on_effect_status_toggled(self, effect, **kwargs):
        pass

    def on_param_value_changed(self, param, **kwargs):
        pass

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        pass
