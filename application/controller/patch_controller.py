from application.dao.bank_dao import BankDao

from application.controller.controller import Controller
from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.update_type import UpdateType


class PatchError(Exception):
    pass


class PatchController(Controller):
    """
    Manage :class:`Patch`, informing the creation, informing the updates
    or deleting and informing it.
    """

    def __init__(self, application):
        super(PatchController, self).__init__(application)
        self.dao = None
        self.banks = None
        self.current = None
        self.notifier = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.app.controller(BanksController)
        self.current = self.app.controller(CurrentController)
        self.notifier = self.app.controller(NotificationController)

    def created(self, patch, token=None):
        """
        Notify all observers that the :class:`Patch` object has been created.

        .. note::

            The patch needs be added in a :class:`Bank` before.

            >>> bank.append(patch)
            >>> patch_controller.created(patch)

        :param Patch patch: Patch created
        :param string token: Request token identifier
        """
        if patch.bank not in self.banks.banks:
            raise PatchError('Bank of patch {} not added in banks manager'.format(patch))

        self._save(patch)
        self._notify_change(patch, UpdateType.CREATED, token)

    def update(self, patch, token=None):
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
        if patch.bank not in self.banks.banks:
            raise PatchError('Bank of patch {} not added in banks manager'.format(patch))

        self._save(patch)

        if self.current.is_current_patch(patch):
            self.current.reload_current_patch()

        self._notify_change(patch, UpdateType.UPDATED, token)

    def replace(self, old_patch, new_patch, token=None):
        """
        Replaces the old patch to new patch and notifies all observers that the
        :class:`Patch` object has UPDATED

        .. note::
            If you're changing a bank that has a current patch,
            the patch should be fully charged and loaded. So, prefer the use
            of other Controllers methods for simple changes.

        :param Patch old_patch: Patch that will be replaced for new_patch
        :param Patch new_patch: Patch that replaces old_patch
        :param string token: Request token identifier
        """
        if old_patch.bank not in self.banks.banks:
            raise PatchError('Bank of old_patch {} not added in banks manager'.format(old_patch))

        if new_patch.bank is not None:
            raise PatchError('Bank of new_patch {} already added in banks manager'.format(new_patch))

        bank = old_patch.bank
        bank.patches[bank.patches.index(old_patch)] = new_patch
        self.update(new_patch, token)

    def delete(self, patch, token=None):
        """
        Remove the :class:`Patch` of your bank.

        .. note::
            If the patch is the current, another patch will be loaded
            and it will be the new current patch.

        :param Patch patch: Patch to be removed
        :param string token: Request token identifier
        """
        if patch.bank not in self.banks.banks:
            raise PatchError('Bank of patch {} not added in banks manager'.format(patch))

        next_patch = None
        if self.current.is_current_patch(patch):
            self.current.to_next_patch()
            next_patch = self.current.current_patch

        bank = patch.bank

        patch_index = patch.bank.patches.index(patch)
        del patch.bank.patches[patch_index]
        self._notify_change(patch, UpdateType.DELETED, token, index=patch_index, origin=bank)

        if next_patch is not None:
            self.current.patch_number = next_patch.bank.patches.index(next_patch)

        self.dao.save(bank, self.banks.banks.index(bank))

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

        # FIXME - Persistence
        # self.dao.save(bank_a)
        # self.dao.save(bank_b)

        # FIXME - Update if is current patch
        # if patch_a or patch_b is current patch, needs update bank index and current patch index

    def _save(self, patch):
        bank = patch.bank
        self.dao.save(bank, self.banks.banks.index(bank))

    def _notify_change(self, patch, update_type, token=None, **kwargs):
        if 'index' not in kwargs:
            kwargs['index'] = patch.bank.patches.index(patch)
        if 'origin' not in kwargs:
            kwargs['origin'] = patch.bank

        self.notifier.patch_updated(patch, update_type, token, **kwargs)
