PedalPi - Application - Dao
===========================

Dao classes provide a means to persist information.

.. warning::

    When creating a component, the model informations are persisted by :class:`Autosaver` class.

.. warning::

    If you need persists and load any data, use the :class:`.ComponentDataController`.

ComponentDao
------------

.. autoclass:: application.dao.component_dao.ComponentDao
   :members:
   :special-members:
   :exclude-members: __weakref__

CurrentDao
----------

.. autoclass:: application.dao.current_dao.CurrentDao
   :members:
   :special-members:
   :exclude-members: __weakref__

PluginsDao
----------

.. autoclass:: application.dao.plugins_dao.PluginsDao
   :members:
   :special-members:
   :exclude-members: __weakref__
