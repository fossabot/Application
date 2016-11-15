PedalPi - Application
=====================

PedalPi - Application is a framework for manager the PedalPi - `Components`_
offers an auto initialization and an updates notification between the components.

.. _Components: https://github.com/PedalPi/Components

Using
-----

.. warning::

    It's deprecated. I am refactoring...

1º Create a folder

.. code-block:: bash

    mkdir my-project
    cd my-project

2º Git clone it

.. code-block:: bash

    git clone http://github.com/PedalPi/Application application

3º Install the requirements

.. code-block:: bash

    pip3 install coverage
    pip3 install gpiozero
    pip3 install rdflib

4º Create your init file (as example ``start.py``)

.. code-block:: python

    sys.path.append('application')

    from application.Application import Application

    application = Application(data_patch="data/", address='localhost')

    application.start()

5º Register something components if neccessary

See the components list in `github Components Project`_.

6º Download and install `mod-host`_

7º Start audio process

.. code-block:: bash

    # In this example, is starting a Zoom g3 series audio interface
    jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
    mod-host &

8º Start application

.. code-block:: bash

    python3 start.py

The Plugins manager observer problem
------------------------------------

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

Extending
---------

It's possible add functionalists or extends the controller with addiction of :class:`Component`.
For list all possibilities, see the `github Components Project`_.

.. _github Components Project: https://github.com/PedalPi/Components

Distributed System
------------------

The connection with `mod-host`_ is over `TCP`_. So it's possible to place a
machine to perform the processing and another to provide the control services.

For example, you have a **Raspberry Pi B+** and a **PC**.
 * The PC in http://10.0.0.100 will process the audio, then it will execute `jack` process, `mod-host` process and the audio interface will be connected to it.
 * The *RPi* will executes :class:`Application` with :class:`Component`, like `Raspberry P0 component`_. Raspberry P0 disposes a simple current patch control.

.. code-block:: python

    application = Application(data_patch="data/", address='10.0.0.100', test=False)

.. _Raspberry P0 component: https://github.com/PedalPi/Raspberry-P0
.. _TCP: https://en.wikipedia.org/wiki/Transmission_Control_Protocol


API
---

Contents:

.. toctree::
   :maxdepth: 2

   application
   controllers
   models
