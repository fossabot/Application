from application.dao.bank_dao import BankDao

from application.controller.controller import Controller
from application.controller.device_controller import DeviceController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.update_type import UpdateType


class EffectController(Controller):
    """
    Manage :class:`Effect`, creating new, deleting or changing status.
    """

    def __init__(self, application):
        super(EffectController, self).__init__(application)
        self.dao = None
        self.current_controller = None
        self.device_controller = None
        self.notifier = None

    def configure(self):
        from application.controller.current_controller import CurrentController
        self.dao = self.app.dao(BankDao)
        self.current_controller = self.app.controller(CurrentController)
        self.device_controller = self.app.controller(DeviceController)
        self.notifier = self.app.controller(NotificationController)

    def create_effect(self, effect, token=None):
        """
        Persists the :class:`Effect` object created in your :class:`Patch`

        .. note::

            The effect needs be added in a :class:`Patch` before.

        :param Effect effect: Effect created and added in your Patch
        :param string token: Request token identifier
        """
        self._update(effect.patch)
        self._notify_change(effect, UpdateType.CREATED, token)

    def delete_effect(self, effect, token=None):
        """
        Remove an :class:`Effect` instance in your :class:`Patch`

        :param Effect effect: Effect will be removed
        :param string token: Request token identifier
        """
        patch = effect.patch

        self._notify_change(effect, UpdateType.DELETED, token)
        patch.effects.remove(effect)

        self._update(patch)

    def toggle_status(self, effect, token=None):
        """
        Toggle the effect status: ``status = not effect.status`` and
        notifies the change

        :param Effect effect: Effect will be toggled your status
        :param string token: Request token identifier
        """
        effect.toggle()

        self._update(effect.patch)
        self.notifier.effect_status_toggled(effect, token)

    def _update(self, patch):
        if patch is None:
            pass

        # self.dao.save(patch.bank)

        # if self.current_controller.is_current_patch(patch):
        #     self.device_controller.loadPatch(patch)
        # FIXME
        ...

    def _notify_change(self, effect, update_type, token):
        self.notifier.effect_updated(effect, update_type, token)

    def connected(self, connection, token=None):
        """
        Informs the :class:`Connection` object has ben created

        :param Connection connection: Connection created
        """
        self.notifier.connection_updated(connection, UpdateType.CREATED, token)

    def disconnected(self, connection, token=None):
        """
        Informs the :class:`Connection` object has ben created

        :param Connection connection: Connection created
        """
        self.notifier.connection_updated(connection, UpdateType.DELETED, token)
