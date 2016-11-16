from dao.BankDao import BankDao

from application.controller.controller import Controller
from application.controller.current_controller import CurrentController
from application.controller.device_controller import DeviceController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.update_type import UpdateType


class PatchController(Controller):
    """
    Manage :class:`Patch`, informing the creation, informing the updates
    or deleting and informing it.
    """

    def __init__(self, application):
        super(PatchController, self).__init__(application)
        self.dao = None
        self.current_controller = None
        self.device_controller = None
        self.notifier = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.current_controller = self.app.controller(CurrentController)
        self.device_controller = self.app.controller(DeviceController)
        self.notifier = self.app.controller(NotificationController)

    def create_patch(self, patch, token=None):
        """
        Persists a new :class:`Patch`.

        .. note::

            The patch needs be added in a :class:`Bank` before.

        :param Patch patch: Patch created
        :param string token: Request token identifier
        """
        # self.dao.save(patch.bank)
        self._notify_change(patch, UpdateType.CREATED, token)

    def update_patch(self, patch, token=None):
        """
        Notify all observers that the :class:`Patch` object has updated
        and persists the new state.

        .. note::
            If you're changing the current patch, the patch should be
            fully charged and loaded. So, prefer the use of other Controllers
            methods for simple changes.

        :param Patch patch: Patch to be updated
        :param string token: Request token identifier
        """
        # self.dao.save(patch.bank)

        # if self.current_controller.is_current_patch(patch):
        #     self.device_controller.loadPatch(patch)

        self._notify_change(patch, UpdateType.UPDATED, token)

    def delete_patch(self, patch, token=None):
        """
        Remove the :class:`Patch` of your bank.

        .. note::
            If the patch is the current, another patch will be loaded
            and it will be the new current patch.

        :param Patch patch: Patch to be removed
        :param string token: Request token identifier
        """
        bank = patch.bank

        # FIXME - Current controller
        #if self.current_controller.is_current_patch(patch):
        #    self.current_controller.to_next_patch()

        patch.bank.patches.remove(patch)
        self._notify_change(patch, UpdateType.DELETED, token)

        # FIXME - Persistance
        #self.dao.save(bank)

    def swap(self, patch_a, patch_b, token=None):
        """
        Swap patch_a with patch_b.

        :param Patch patch_a: Patch to be swapped with patch_b
        :param Patch patch_b: Patch to be swapped with patch_a
        :param string token: Request token identifier
        """
        bank_a = patch_a.bank
        bank_b = patch_b.bank

        index_a = bank_a.patches.index(patch_a)
        index_b = bank_b.patches.index(patch_b)

        bank_a.patches[index_a], bank_b.patches[index_b] = bank_b.patches[index_b], bank_a.patches[index_a]

        self.notifier.patch_updated(patch_a, UpdateType.UPDATED, token=token)
        self.notifier.patch_updated(patch_b, UpdateType.UPDATED, token=token)

        # FIXME - Persistance
        # self.dao.save(bank_a)
        # self.dao.save(bank_b)

        # FIXME - Update if is current patch
        # if patch_a or patch_b is current patch, needs update bank index and current patch index

    def _notify_change(self, patch, update_type, token=None):
        self.notifier.patch_updated(patch, update_type, token)
