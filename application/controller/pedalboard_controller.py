from application.dao.bank_dao import BankDao

from application.controller.controller import Controller
from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.update_type import UpdateType


class PedalboardError(Exception):
    pass


class PedalboardController(Controller):
    """
    Manage :class:`Pedalboard`, informing the creation, informing the updates
    or deleting and informing it.
    """

    def __init__(self, application):
        super(PedalboardController, self).__init__(application)
        self.dao = None
        self.banks = None
        self.current = None
        self.notifier = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.app.controller(BanksController)
        self.current = self.app.controller(CurrentController)
        self.notifier = self.app.controller(NotificationController)

    def created(self, pedalboard, token=None):
        """
        Notify all observers that the :class:`Pedalboard` object has been created.

        .. note::

            The pedalboard needs be added in a :class:`Bank` before.

            >>> bank.append(pedalboard)
            >>> pedalboard_controller.created(pedalboard)

        :param Pedalboard pedalboard: Pedalboard created
        :param string token: Request token identifier
        """
        if pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of pedalboard {} not added in banks manager'.format(pedalboard))

        self._save(pedalboard)
        self._notify_change(pedalboard, UpdateType.CREATED, token)

    def update(self, pedalboard, token=None, reload=True):
        """
        Notify all observers that the :class:`Pedalboard` object has updated
        and persists the new state.

        .. note::
            If you're changing the current pedalboard, the pedalboard should be
            fully charged and loaded. So, prefer the use of other Controllers
            methods for simple changes.

        :param Pedalboard pedalboard: Pedalboard to be updated
        :param string token: Request token identifier
        :param bool reload: If it's the current pedalboard, is necessary reload the plugins?
        """
        if pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of pedalboard {} not added in banks manager'.format(pedalboard))

        self._save(pedalboard)

        if self.current.is_current_pedalboard(pedalboard) and reload:
            self.current.reload_current_pedalboard()

        self._notify_change(pedalboard, UpdateType.UPDATED, token)

    def replace(self, old_pedalboard, new_pedalboard, token=None):
        """
        Replaces the old pedalboard to new pedalboard and notifies all observers that the
        :class:`Pedalboard` object has UPDATED

        .. note::
            If you're changing a bank that has a current pedalboard,
            the pedalboard should be fully charged and loaded. So, prefer the use
            of other Controllers methods for simple changes.

        :param Pedalboard old_pedalboard: Pedalboard that will be replaced for new_pedalboard
        :param Pedalboard new_pedalboard: Pedalboard that replaces old_pedalboard
        :param string token: Request token identifier
        """
        if old_pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of old_pedalboard {} not added in banks manager'.format(old_pedalboard))

        if new_pedalboard.bank is not None:
            raise PedalboardError('Bank of new_pedalboard {} already added in banks manager'.format(new_pedalboard))

        bank = old_pedalboard.bank
        bank.pedalboards[bank.pedalboards.index(old_pedalboard)] = new_pedalboard
        self.update(new_pedalboard, token)

    def delete(self, pedalboard, token=None):
        """
        Remove the :class:`Pedalboard` of your bank.

        .. note::
            If the pedalboard is the current, another pedalboard will be loaded
            and it will be the new current pedalboard.

        :param Pedalboard pedalboard: Pedalboard to be removed
        :param string token: Request token identifier
        """
        if pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of pedalboard {} not added in banks manager'.format(pedalboard))

        # Get next pedalboard if the removed is the current pedalboard
        next_pedalboard = None
        if self.current.is_current_pedalboard(pedalboard):
            self.current.to_next_pedalboard()
            next_pedalboard = self.current.current_pedalboard

        bank = pedalboard.bank

        # Remove
        pedalboard_index = pedalboard.index
        del pedalboard.bank.pedalboards[pedalboard_index]
        self._notify_change(pedalboard, UpdateType.DELETED, token, index=pedalboard_index, origin=bank)

        # Update current pedalboard
        #only_pedalboard_bank_has_removed = len(bank.pedalboards) == 0
        #if only_pedalboard_bank_has_removed:
        #    self.current.remove_current(token=token)

        #elif next_pedalboard is not None:
        if next_pedalboard is not None:
            self.current.pedalboard_number = next_pedalboard.index

        self.dao.save(bank, self.banks.banks.index(bank))

    def swap(self, pedalboard_a, pedalboard_b, token=None):
        """
        Swap pedalboard_a with pedalboard_b.

        :param Pedalboard pedalboard_a: Pedalboard to be swapped with pedalboard_b
        :param Pedalboard pedalboard_b: Pedalboard to be swapped with pedalboard_a
        :param string token: Request token identifier
        """
        bank_a = pedalboard_a.bank
        bank_b = pedalboard_b.bank

        index_a = bank_a.index
        index_b = bank_b.index

        bank_a.pedalboards[index_a], bank_b.pedalboards[index_b] = bank_b.pedalboards[index_b], bank_a.pedalboards[index_a]

        self._notify_change(pedalboard_a, UpdateType.UPDATED, token=token)
        self._notify_change(pedalboard_b, UpdateType.UPDATED, token=token)

        # FIXME - Persistence
        # self.dao.save(bank_a)
        # self.dao.save(bank_b)

        # FIXME - Update if is current pedalboard
        # if pedalboard_a or pedalboard_b is current pedalboard, needs update bank index and current pedalboard index

    def _save(self, pedalboard):
        bank = pedalboard.bank
        self.dao.save(bank, self.banks.banks.index(bank))

    def _notify_change(self, pedalboard, update_type, token=None, **kwargs):
        index = kwargs.pop('index') if 'index' in kwargs else pedalboard.index
        origin = kwargs.pop('origin') if 'origin' in kwargs else pedalboard.bank

        self.notifier.pedalboard_updated(pedalboard, update_type, index=index, origin=origin, token=token, **kwargs)
