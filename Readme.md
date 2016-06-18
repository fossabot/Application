# PedalPi - Application

[![Build Status](https://travis-ci.org/PedalPi/Application.svg?branch=master)](https://travis-ci.org/PedalPi/Application) [![Coverage Status](https://coveralls.io/repos/github/PedalPi/Application/badge.svg?branch=master)](https://coveralls.io/github/PedalPi/Application?branch=master) [![Code Health](https://landscape.io/github/PedalPi/Application/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/Application/master) [![codecov](https://codecov.io/gh/PedalPi/Application/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/Application)

## Using

```
#sudo apt-get install guitarix

killall -9 jackd
killall -9 mod-host
jackd -P70 -p16 -t2000 -dalsa -dhw:Series -p128 -n3 -r44100 -s &
./mod-host
qjackctl &
```