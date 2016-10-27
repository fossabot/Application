PedalPi - Application
=====================

API for pythonic management with LV2 audio plugins using `mod-host`_.

.. _mod-host: https://github.com/moddevices/mod-host

Contents:

.. toctree::
   :maxdepth: 2

   controllers
   models

Using
-----

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

    from application.Application import Application

    address = 'localhost'

    application = Application(data_patch="data/", address=address, test=True)

    application.start()

5º Register something components

TODO - Add components list

6º Download and install `mod-host`

7º Start audio process

.. code-block:: bash

    jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
    mod-host

8º Start application

.. code-block:: bash

    python3 start.py

Application
-----------

.. autoclass:: Application.Application
  :members:
