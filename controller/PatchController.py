from dao.BankDao import BankDao

from controller.Controller import Controller
from controller.CurrentController import CurrentController
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController

from model.UpdatesObserver import UpdateType


class PatchController(Controller):
    """
    Manage :class:`Patch`, creating new, updating or deleting.
    """

    def __init__(self, application):
        super(PatchController, self).__init__(application)
        self.dao = None
        self.currentController = None
        self.deviceController = None
        self.notificationController = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def create_patch(self, patch, token=None):
        """
        Persists a new :class:`Patch`. The patch needs be added in a :class:`Bank`
        before.

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

        # if self.currentController.isCurrentPatch(patch):
        #     self.deviceController.loadPatch(patch)

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
        #if self.currentController.isCurrentPatch(patch):
        #    self.currentController.toNextPatch()

        patch.bank.patches.remove(patch)
        self._notify_change(patch, UpdateType.DELETED, token)

        # FIXME - Persistance
        #self.dao.save(bank)

    def swapPatches(self, patchA, patchB):
        """
        .. deprecated::
            Don't use

        Swap patchA order to patchB order
        """
        patchA.bank.swapPatches(patchA, patchB)
        self.dao.save(patchA.bank)

    def _notify_change(self, patch, update_type, token=None):
        self.notificationController.notifyPatchUpdated(patch, update_type, token)
