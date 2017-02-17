from application.controller.controller import Controller


class NotificationController(Controller):
    """
    Notifies request changes to all :class:`UpdatesObserver` registered
    than not contains the same request _token_.
    """

    def __init__(self, app):
        super().__init__(app)
        self.observers = []

    def configure(self):
        pass

    def register(self, observer):
        """
        Register an observer

        :param Notification observer: An observer that will be received the changes
        """
        self.observers.append(observer)

    def unregister(self, observer):
        """
        Unregister an observer
        
        :param Notification observer: An observer that not will be more received the changes
        """
        self.observers.remove(observer)

    def is_requester(self, observer, token):
        """
        Verify if the observer is the requester change (if observer contains
        same token that token informed)

        :param UpdatesObserver observer:
        :param string token: Request token identifier
        :return: The requisiton is realized by observer?
        """
        return observer.token is not None and observer.token == token

    ########################
    # Notify methods
    ########################
    def current_pedalboard_changed(self, pedalboard, token=None):
        """
        Notify current pedalboard change.

        :param Pedalboard pedalboard: New current pedalboard
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_current_pedalboard_changed(pedalboard, token)

    def bank_updated(self, bank, update_type, token=None, **kwargs):
        """
        Notify changes in :class:`Bank`.

        :param Bank bank: Bank changed.
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_bank_updated(bank, update_type, token, **kwargs)

    def pedalboard_updated(self, pedalboard, update_type, token=None, **kwargs):
        """
        Notify changes in :class:`Pedalboard`.

        :param Pedalboard pedalboard: Pedalboard changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_pedalboard_updated(pedalboard, update_type, token, **kwargs)

    def effect_updated(self, effect, update_type, token=None, **kwargs):
        """
        Notify changes in :class:`Effect`.

        :param Effect effect: Effect changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_effect_updated(effect, update_type, token, **kwargs)

    def effect_status_toggled(self, effect, token=None):
        """
        Notify :class:`Effect` status toggled.

        :param Effect effect: Effect when status has been toggled
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_effect_status_toggled(effect, token)

    def param_value_changed(self, param, token=None, **kwargs):
        """
        Notify :class:`Param` value change.

        :param Param param: Param with value changed
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_param_value_changed(param, token, **kwargs)

    def connection_updated(self, pedalboard, connection, update_type, token=None):
        """
        Notify :class:`Connection` addictions and removals.

        :param Pedalboard pedalboard: Pedalboard where has added or removed a connection
        :param Connection connection: Connection added or removed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_connection_updated(pedalboard, connection, update_type, token)
