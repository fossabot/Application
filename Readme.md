# PedalPi - Application

[![Build Status](https://travis-ci.org/PedalPi/Application.svg?branch=master)](https://travis-ci.org/PedalPi/Application) [![Documentation Status](https://readthedocs.org/projects/pedalpi-application/badge/?version=latest)](http://pedalpi-application.readthedocs.io/en/latest/?badge=latest) [![Code Health](https://landscape.io/github/PedalPi/Application/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/Application/master) [![codecov](https://codecov.io/gh/PedalPi/Application/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/Application) 

API for pythonic management with LV2 audio plugins using [mod-host](https://github.com/modddevices/mod-host).

For API documentation, see [Application Documentation](http://pedalpi-application.readthedocs.io/en/latest/).

## Local test

```bash
coverage3 run --source=architecture,controller,dao,model setup.py test
coverage3 report
coverage3 html
firefox htmlcov/index.html
```

## Using

http://pedalpi-application.readthedocs.io/en/latest/#using

### Initializing audio processes

```
jackd -P70 -p16 -t2000 -dalsa -dhw:Series -p128 -n3 -r44100 -s &
./mod-host &

# Optionally, view the graph connections with qjackctl
qjackctl &
```

### For retry
```
killall -9 jackd
killall -9 mod-host
# execute "Usign" steps
```

## Documentation

This project uses [Sphinx](www.sphinx-doc.org) and [Read the doc](readthedocs.org).

For local documentation build

```bash
cd docs
make html
```

For view the last documentation, access http://pedalpi-application.readthedocs.io/.