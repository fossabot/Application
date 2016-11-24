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

    def is_requisitor(self, observer, token):
        """
        Verify if the observer is the requisitor change (if observer contains
        same token that token informed)

        :param UpdatesObserver observer:
        :param string token: Request token identifier
        :return: The requisiton is realized by observer?
        """
        return observer.token is not None and observer.token == token

    ########################
    # Notify methods
    ########################
    def current_patch_changed(self, patch, token=None):
        """
        Notify current patch change.

        :param Patch patch: New current patch
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requisitor(observer, token):
                observer.on_current_patch_changed(patch, token)

    def bank_updated(self, bank, update_type, token=None, **kwargs):
        """
        Notify changes in :class:`Bank`.

        :param Bank bank: Bank changed.
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requisitor(observer, token):
                observer.on_bank_updated(bank, update_type, token, **kwargs)

    def patch_updated(self, patch, update_type, token=None, **kwargs):
        """
        Notify changes in :class:`Patch`.

        :param Patch patch: Patch changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requisitor(observer, token):
                observer.on_patch_updated(patch, update_type, token, **kwargs)

    def effect_updated(self, effect, update_type, token=None, **kwargs):
        """
        Notify changes in :class:`Effect`.

        :param Effect effect: Effect changed
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requisitor(observer, token):
                observer.on_effect_updated(effect, update_type, token, **kwargs)

    def effect_status_toggled(self, effect, token=None):
        """
        Notify :class:`Effect` status toggled.

        :param Effect effect: Effect when status has been toggled
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requisitor(observer, token):
                observer.on_effect_status_toggled(effect, token)

    def param_value_changed(self, param, token=None, **kwargs):
        """
        Notify :class:`Param` value change.

        :param Param param: Param with value changed
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requisitor(observer, token):
                observer.on_param_value_changed(param, token, **kwargs)

    def connection_updated(self, connection, update_type, token=None):
        for observer in self.observers:
            if not self.is_requisitor(observer, token):
                observer.on_connection_updated(connection, update_type, token)
