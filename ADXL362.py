############################################################
### Library for Communicating with ADXL362 Accelerometer ###
### for Raspberry Pi using spidev                        ###
###                                                      ###
### Authors: Sam Zeckendorf                              ###
###          Nathan Tarrh                                ###
###    Date: 3/29/2014                                   ###
############################################################

# spidev is the Raspberry Pi spi communication library
import spidev
import time
import RPi.GPIO as gpio

class ADXL362:

    def __init__(self):

        # establish slave pin for enable
        self.slave_pin = 8

        # configure gpio interface
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.slave_pin, gpio.OUT)

        # init spi for communication
        self.spi = spidev.SpiDev()

        # Set clock phase and polarity to default
        self.spi.mode = 0b00 
        #time.sleep(.5)

        self.spi_write_reg(0x1F, 0x52)
        #time.sleep(.01)

        print 'Soft reset'
    
    def spi_write_reg(self, address, value):
        ''' Write value to address
            Arguments:
                - address: Hexidecimal value of register address
                -   value: Desired hexidecimal byte to write
        '''

        # Set select line low to enable communication 
        gpio.output(self.slave_pin, gpio.LOW)
        
        # Send instruction (write)
        self.spi.xfer([0x0A])

        # Send address
        self.spi.xfer([address])
        
        # send value
        self.spi.xfer([value])

        # Set select line high to terminate connection
        gpio.output(self.slave_pin, gpio.HIGH)

        
    def spi_read_reg(self, address):
        ''' Read contents of register at specified address
            Arguments:
                - address: Hexidecimal value of register address
            Returns:
                - value at address
        '''
        
        # Set select line low to enable communication 
        gpio.output(self.slave_pin, gpio.LOW)
        
        # Send instruction (write)
        self.spi.xfer([0x0B])

        # Send address
        self.spi.xfer([address])
        
        # Transfer 0x00 to read response
        response = self.spi.xfer([0x00])

        # Set select line high to terminate connection
        gpio.output(self.slave_pin, gpio.HIGH)
    
        return response

    def begin_measure(self):
        ''' Turn on measurement mode, required after reset
        '''
        
        # Read in current value in power control register
        pc_reg = self.spi_read_reg(0x2D)
        
        # Mask measurement mode onto power control buffer
        pc_reg_new = pc_reg | 0x02

        # Write new power control buffer to register
        self.spi_write_reg(0x2D, pc_reg_new)

        time.sleep(.01)

    def read_x(self):
        ''' Read the x value
            Returns:
                - Value of ug in x direction
        '''
        x = self.spi_read_two(0x0E)
        return x

    def read_y(self):
        ''' Read the y value
            Returns:
                - Value of ug in the y direction
        '''
        y = self.spi_read_two(0x10)
        return y

    def read_z(self):
        ''' Read the z value
            Returns:
                - Value of ug in the z direction
        '''
        z = self.spi_read_two(0x12)
        return z

    def read_temp(self):
        ''' Read the temperature value (for calibration/correlation)
            Returns:
                - Internal device temperature
        '''
        temp = self.spi_read_two(0x14)
        return temp

    def read_xyz(self):
        ''' Read x, y, and z data in burst mode. A burst read is required to
            guarantee all measurements correspond to the same sample time.
            Returns:
                - Tuple with x, y, z, and temperature data
        '''
        # Open communication
        gpio.output(self.slave_pin, gpio.LOW)

        # Send read instruction
        self.spi.xfer([0x0B])

        # Start at x data register
        self.spi.xfer([0x0E])

        # Read each vector in order
        x = self.spi.xfer([0x00])[0]
        x = x + (self.spi.xfer([0x00])[0] << 8)
        y = self.spi.xfer([0x00])[0]
        y = y + (self.spi.xfer([0x00])[0] << 8)
        z = self.spi.xfer([0x00])[0]
        z = z + (self.spi.xfer([0x00])[0] << 8)
        temp = self.spi.xfer([0x00])[0]
        temp = temp + (self.spi.xfer([0x00])[0] << 8)

        # Close communication
        gpio.output(self.slave_pin, gpio.LOW)

        return (x, y, z, temp)
        
    def spi_read_two(self, address):
        ''' Read two sequential registers
            Arguments: 
                - address: Hexidecimal address of first register to read from
            Returns: 
                - Value contained within said two registers
        '''
        
        # Set slave select to LOW for communication 
        gpio.output(self.slave_pin, gpio.LOW)
        
        # Send read instruction
        self.spi.xfer([0x0B])
        
        # Send address to be read from
        self.spi.xfer([address])
        
        # Read first register 
        value = self.spi.xfer([0x00])
        
        # Read second register into bit-shifted first value
        value = value + (self.spi.xfer([0x00]) << 8)
        
        # Close slave select
        gpio.output(self.slave_pin, gpio.HIGH)
        return value

    def spi_write_two(self, address, value):
        ''' Write to two sequential registers
            Arguments: 
                - address: Hexidecimal address of first register to write from
                -   value: Value to be written
        '''
        # Split value into high and low bytes for writing
        high_byte = value >> 8
        low_byte = value & 0xFF
         
        # Set slave select to LOW for communication 
        gpio.output(self.slave_pin, gpio.LOW)
        
        # Send write instruction
        self.spi.xfer([0x0A])
        
        # Send address to be written to
        self.spi.xfer([address])
        
        # Write to low register 
        self.spi.xfer(low_byte)

        # Write to high register 
        self.spi.xfer(high_byte)
        
        # Close slave select
        gpio.output(self.slave_pin, gpio.HIGH)
        return value

