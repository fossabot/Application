PedalPi - Application
=====================

.. image:: https://travis-ci.org/PedalPi/Application.svg?branch=master
    :target: https://travis-ci.org/PedalPi/Application
    :alt: Build Status

.. image:: https://readthedocs.org/projects/pedalpi-application/badge/?version=latest
    :target: http://pedalpi-application.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/PedalPi/Application/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PedalPi/Application
    :alt: Code coverage

.. image:: https://landscape.io/github/PedalPi/Application/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PedalPi/Application/master
    :alt: Code Health

API for pythonic management with LV2 audio plugins using `mod-host`_ and `plugins manager`_.

.. _mod-host: https://github.com/modddevices/mod-host
.. _plugins manager: http://pedalpi-pluginsmanager.readthedocs.io/

Documentation
-------------

Access http://pedalpi-application.readthedocs.io/ for the last documentation.

Maintenance
-----------

Test
****

The purpose of the tests is:

* Check if the notifications are working, since the module plugins manager is responsible for testing the models;
* Serve as a sample basis.

.. code-block:: bash

    coverage3 run --source=application setup.py test
    coverage3 report
    coverage3 html
    firefox htmlcov/index.html

Generate documentation
**********************

This project uses `Sphinx`_ + `Read the Docs`_.

You can generate the documentation in your local machine:

.. code-block:: bash

    pip3 install sphinx

    cd docs
    make html

    firefox build/html/index.html

.. _Sphinx: http://www.sphinx-doc.org/
.. _Read the Docs: http://readthedocs.org
