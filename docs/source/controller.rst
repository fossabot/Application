PedalPi - Application - Controller
==================================

Token
-----

`pluginsmanager`_ can notifies they changes. As an example, if a connection
between effects is created, plugins manager notifies its observers about the change.

This is how :class:`pluginsmanager.mod_host.mod_host.ModHost` and :class:`pluginsmanager.observer.auto_saver.Autosaver`
know when a change occurs.

These observers work passively: they only receive updates, not using the `pluginsmanager`_
api to change the state of the application.

Man-Machine Interfaces are usually active: they need to change the state of the application.
As an example, a button that leaves bypass an effect.
They also need to receive notifications, so that the information presented
to the user can be updated in accordance with changes made by other interfaces.

In these cases, is necessary in a change notifiers all except the one who caused the change.

As example, a multi-effects uses `Raspberry-P1`_ for physical management and
`WebService`_ for a controller with `Apk`_ controller. If they uses only
`pluginsmanager`, a toggle status effect change in a Raspberry-P1 will
informs WebService and unreasonably Raspberry-P1.

`pluginsmanager`_ has a solution to this problem::

    >>> class MyAwesomeObserver(UpdatesObserver):

    >>>     def __init__(self, message):
    >>>         self.message = message
    >>>
    >>>     def on_bank_updated(self, bank, update_type, **kwargs):
    >>>         print(self.message)
    >>>
    >>>
    >>> observer1 = MyAwesomeObserver("Hi! I am observer1")
    >>> observer2 = MyAwesomeObserver("Hi! I am observer2")
    >>>
    >>> manager = BanksManager()
    >>> manager.register(observer1)
    >>> manager.register(observer2)
    >>>
    >>> bank = Bank('Bank 1')
    >>> manager.banks.append(bank)
    "Hi! I am observer1"
    "Hi! I am observer2"
    >>> with observer1:
    >>>     del manager.banks[0]
    "Hi! I am observer2"
    >>> with observer2:
    >>>     manager.banks.append(bank)
    "Hi! I am observer1"

However, it is not reliable since it is not thread safe.

Application uses an explicit way of reporting notifications
via `tokens` - unique strings that identify observers.
Your API provides methods that change the state of the application
that receive a token as a parameter.
A change with an informed token is not propagated to an observer who has this token::

    >>> class MyAwesomeObserver(ApplicationObserver):
    >>>     def __init__(self, application, token, name):
    >>>         super(ActionsFacade, self).__init__()
    >>>         self._token = token
    >>>         self.name = name
    >>>
    >>>     @property
    >>>     def token(self):
    >>>         return self._token
    >>>
    >>>     def on_effect_status_toggled(self, effect, **kwargs):
    >>>         print(self.name)
    >>>
    >>>     ...
    >>>
    >>> observer1 = MyAwesomeObserver('observer-1', 'Observer 1 method called!')
    >>> observer2 = MyAwesomeObserver('observer-2', 'Observer 2 method called!')
    >>>
    >>> notification_controller = application.controller(NotificationController)
    >>> notification_controller.register(observer1)
    >>> notification_controller.register(observer2)
    >>>
    >>> effects_controller = application.controller(EffectController)
    >>> effects_controller.toggle_status(reverb)
    'Observer 1 method called!'
    'Observer 2 method called!'
    >>> effects_controller.toggle_status(reverb, observer1.token)
    'Observer 2 method called!'
    >>> effects_controller.toggle_status(reverb, observer2.token)
    'Observer 1 method called!'

.. _pluginsmanager: https://github.com/PedalPi/PluginsManager
.. _Raspberry-P1: https://github.com/PedalPi/Raspberry-P1
.. _WebService: https://github.com/PedalPi/WebService
.. _Apk: https://github.com/PedalPi/Apk
.. _mod-host: https://github.com/moddevices/mod-host


Controller
----------

.. autoclass:: application.controller.controller.Controller
   :members:
   :special-members:
   :exclude-members: __weakref__

ComponentDataController
-----------------------

.. autoclass:: application.controller.component_data_controller.ComponentDataController
   :members:
   :special-members:
   :exclude-members: __weakref__

CurrentController
-----------------

.. autoclass:: application.controller.current_controller.CurrentController
   :members:
   :special-members:
   :exclude-members: __weakref__

DeviceController
----------------

.. autoclass:: application.controller.device_controller.DeviceController
   :members:
   :special-members:
   :exclude-members: __weakref__

PluginsController
-----------------

.. autoclass:: application.controller.plugins_controller.PluginsController
   :members:
   :special-members:
   :exclude-members: __weakref__

.. autoclass:: application.controller.plugins_controller.PluginTechnology
   :members:
   :special-members:
   :exclude-members: __weakref__
