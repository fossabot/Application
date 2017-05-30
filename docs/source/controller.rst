PedalPi - Application - Controller
==================================

Notification scope
------------------

`pluginsmanager`_ can notifies they changes. As an example, if a connection
between effects is created, plugins manager notifies its observers about the change.

This is how :class:`~pluginsmanager.mod_host.mod_host.ModHost` and
:class:`~pluginsmanager.observer.auto_saver.Autosaver` know when a change occurs.

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

A quick review will be given ahead. For more details, see the `pluginsmanager observer
documentation`_.

.. _pluginsmanager observer documentation: http://pedalpi-pluginsmanager.readthedocs.io/en/latest/observer.html

`pluginsmanager`_ has a solution to this problem. Defining a observer::


    class MyAwesomeObserver(UpdatesObserver):

        def __init__(self, message):
            self.message = message

        def on_bank_updated(self, bank, update_type, **kwargs):
            print(self.message)

        # Defining others abstract methods
        ...


Using::

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

Using **application**, the process changes a bit. Because pluginsmanager does not support the current
pedalboard change notifications, clients should extend from :class:`.ApplicationObserver`,
a specialization that adds this functionality::

    class MyAwesomeObserver(ApplicationObserver):

        def __init__(self, message):
            self.message = message

        def on_current_pedalboard_changed(self, pedalboard, **kwargs):
            print('Pedalboard changed!')

        def on_bank_updated(self, bank, update_type, **kwargs):
            print(self.message)

        # Defining others abstract methods
        ...


To correctly register ApplicationObserver, you must use :meth:`.Application.register_observer`
(or :meth:`.Component.register_observer`)::

    >>> observer1 = MyAwesomeObserver("Hi! I am observer1")
    >>> observer2 = MyAwesomeObserver("Hi! I am observer2")
    >>>
    >>> application.register_observer(observer1)
    >>> application.register_observer(observer2)

.. note::

    Registering directly to the pluginsmanager will result in not receiving updates
    defined by :class:`.ApplicationObserver`

Using::

    >>> manager = application.manager
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

.. warning::


    The operations performed by PluginsManager **are not atomic**.
    This architectural constraint was based on the experienced experience
    that one user will use the system at a time.
    In this way, try not to abuse the concurrence.

    If you are having problems while doing this, `let us know`_.

.. _let us know: https://github.com/PedalPi/Application/issues/
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
