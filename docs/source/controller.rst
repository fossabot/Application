PedalPi - Application - Controller
==================================

The Plugins manager observer problem
------------------------------------

FIXME - Explain **token**

`pluginsmanager`_ can notifies they changes, but in a case that many
uses the plugins manager objects, is necessary in a change notifiers
all except the one who caused the change.

As example, a multi-effects uses `Raspberry-P1`_ for physical management and
`WebService`_ for a controller with `Apk`_ controller. If they uses only
`plugins manager`, a toggle status effect change in a Raspberry-P0 will
informs WebService and unreasonably Raspberry-P1.

Using the Application controllers for management and notification, the problem
will be avoived.

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

BanksController
---------------

.. autoclass:: application.controller.banks_controller.BanksController
   :members:
   :special-members:

ComponentDataController
-----------------------

.. autoclass:: application.controller.component_data_controller.ComponentDataController
   :members:
   :special-members:


CurrentController
-----------------

.. autoclass:: application.controller.current_controller.CurrentController
   :members:
   :special-members:

DeviceController
----------------

.. autoclass:: application.controller.device_controller.DeviceController
   :members:
   :special-members:

EffectController
----------------

.. autoclass:: application.controller.effect_controller.EffectController
   :members:
   :special-members:

NotificationController
----------------------

.. autoclass:: application.controller.notification_controller.NotificationController
   :members:
   :special-members:

ParamController
---------------

.. autoclass:: application.controller.param_controller.ParamController
   :members:
   :special-members:

PedalboardController
--------------------

.. autoclass:: application.controller.pedalboard_controller.PedalboardController
   :members:
   :special-members:

PluginsController
-----------------

.. autoclass:: application.controller.plugins_controller.PluginsController
   :members:
   :special-members:

.. autoclass:: application.controller.plugins_controller.PluginTechnology
   :members:
   :special-members:
