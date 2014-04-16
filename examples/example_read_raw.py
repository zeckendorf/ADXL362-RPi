############################################################
### Example for Communicating with ADXL362 Accelerometer ###
### for Raspberry Pi using ADXL362.py                    ###
###                                                      ###
### Authors: Sam Zeckendorf                              ###
###          Nathan Tarrh                                ###
###    Date: 3/29/2014                                   ###
############################################################

import ../ADXL362
import time

accel = ADXL362.ADXL362()
accel.begin_measure()

while True:
    print accel.read_xyz()
    time.sleep(.01)
