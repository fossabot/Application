# PedalPi - Application

[![Build Status](https://travis-ci.org/PedalPi/Application.svg?branch=master)](https://travis-ci.org/PedalPi/Application) [![Code Health](https://landscape.io/github/PedalPi/Application/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/Application/master) [![codecov](https://codecov.io/gh/PedalPi/Application/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/Application)

## Using

```
jackd -P70 -p16 -t2000 -dalsa -dhw:Series -p128 -n3 -r44100 -s &
./mod-host
qjackctl &
```

### For retry
```
killall -9 jackd
killall -9 mod-host
# execute "Usign" steps
```

## Local test

```bash
coverage3 run --source=architecture,controller,dao,model setup.py test
coverage3 report
coverage3 html
firefox htmlcov/index.html
```