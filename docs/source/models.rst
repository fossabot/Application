PedalPi - Application - Models
==============================

This page contains the model classes.

.. graphviz::

   digraph classes {
       graph [rankdir=TB];
       node [shape=rect, style=filled, color="#298029", fontname=Sans, fontcolor="#ffffff", fontsize=10];

       Banks->Bank [dir="forward", arrowhead="odiamond", arrowtail="normal"];
       Bank->Effect [dir="forward", arrowhead="odiamond", arrowtail="normal"];
       Param->Effect [dir="backward", arrowhead="diamond", arrowtail="normal"];
   }

.. warning::
   It is strongly recommended that you use :class:`Controller`
   to change the status of any of the Models than directly change them.

   Changes in a Models directy **not will be** persisted and
   **not will notifies** the Application :class:`UpdateObservers`

Bank
----

.. autoclass:: model.Bank.Bank
   :members:
   :special-members:

Banks
-----

.. autoclass:: model.Banks.Banks
   :members:
   :special-members:

Effect
------

.. autoclass:: model.Effect.Effect
   :members:
   :special-members:

Param
-----

.. autoclass:: model.Param.Param
   :members:
   :special-members:

Patch
-----

.. autoclass:: model.Patch.Patch
   :members:
   :special-members:

UpdatesObserver
---------------

.. autoclass:: model.UpdatesObserver.UpdatesObserver
   :members:
   :special-members:

.. autoclass:: model.UpdatesObserver.UpdateType
   :members:
   :special-members:
