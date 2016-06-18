# PedalPi - Application

[![Build Status](https://travis-ci.org/PedalPi/Application.svg?branch=master)](https://travis-ci.org/PedalPi/Application) [![Build Status](https://travis-ci.org/PedalPi/Application.svg?branch=master)](https://travis-ci.org/PedalPi/Application)

## Using

```
#sudo apt-get install guitarix

killall -9 jackd
killall -9 mod-host
jackd -P70 -p16 -t2000 -dalsa -dhw:Series -p128 -n3 -r44100 -s &
./mod-host
qjackctl &
```