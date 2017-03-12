from abc import ABCMeta, abstractmethod


class ApplicationObserver(metaclass=ABCMeta):
    """
    The :class:`ApplicationObserver` extends :class:`UpdatesObserver`.
    It is an abstract class definition for treatment of changes in some class model.
    Your methods are called when occurs any change in Bank, Pedalboard, Effect, etc.

    To do this, it is necessary that the :class:`ApplicationObserver` objects
    be registered in some manager, so that it reports the changes. An
    example of a manager is :class:`NotificationController`.

    :class:`NotificationController`, comparing with, :class:`UpdatesObserver`
    add TOKEN. Each observer should have a unique token. This token will differentiate who
    is making requests so the manager does not notify you back.

    For example, if a component requires the manager to have an effect change its
    state (`effect.active = not effect.active`), it is not necessary for the manager
    to inform the component of the change. If the component was informed, it might not know
    that it was the one that requested the change and possibly would update its interface
    erroneously.
    """

    def __init__(self):
        super(ApplicationObserver, self).__init__()
        self.token = None

    @abstractmethod
    def on_current_pedalboard_changed(self, pedalboard, token=None):
        pass
