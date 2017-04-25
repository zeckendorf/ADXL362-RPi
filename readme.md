# ADXL362 RPi Library
This library provides boilerplate for interfacing with raw data from ADXL362 3-axis accelerometer. 

#### Requirements:
* spidev
* python2.7 or python3.x

#### Usage: 
``` python
$ >>>: import ADXL362 as accel
$ >>>: a = accel.ADXL362()
$ >>>: a.begin_measure()
$ >>>: a.read_xyz()
$ >>>: a.read_x()
$ >>>: a.read_y()
$ >>>: a.read_z()
$ >>>: a.read_temp()
```

