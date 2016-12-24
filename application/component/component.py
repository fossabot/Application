from abc import ABCMeta, abstractmethod

from application.controller.notification_controller import NotificationController


class Component(metaclass=ABCMeta):

    def __init__(self, application):
        self.application = application

    @abstractmethod
    def init(self):
        """
        Initialize this component
        """
        pass

    def controller(self, controller):
        return self.application.controller(controller)

    def register_observer(self, observer):
        """
        Register an observer in :class:`Application` by :class:`NotificationController`.
        Observers will be notified of the changes requested in the application API.

        Obs: If a observer contains a _token_ and the request informs the same _token_
        the observer not will be notified.

        :param UpdatesObserver observer:
        """
        self.controller(NotificationController).register(observer)

    def unregister_observer(self, observer):
        """
        Unregister an observer in :class:`Application` by :class:`NotificationController`.
        The observer not will be more notified of the changes requested in the application API.

        :param UpdatesObserver observer:
        """
        self.controller(NotificationController).unregister(observer)
