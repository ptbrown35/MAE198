'''
* File: urm07_read_filtered.py
* Author: Parker Brown
* Date: 12/7/2017
* Course: MAE 198, Fall 2017
* Description: Script reads distance measurements from sensor at specified device
* address and applies a first order low pass filter to the raw data.
* Documentation for the sensors can be found here:
* https://www.dfrobot.com/wiki/index.php/URM07-UART_Ultrasonic_Sensor_SKU:_SEN0153
* URM07 sensors must be connected to the Raspberry Pi UART interface, header pins
* 8 (TX) and 10 (RX), and the 3.3V power supply.
'''

import serial
import time

filter_coeff = [0.6, 0.4] # Low Pass filter coefficients
sample_time = 0.05 # Sample Rate: 20 Hz

# Command Frame Header
header_H = 0x55 # Header High
header_L = 0xAA # Header Low

# Device Addresses
#device_addr = 0xAB # Address: Generic

data_length = 0x00 # Data length
get_dist_cmd = 0x02 # Command: Read Distance
get_temp_cmd = 0x03 # Command: Read Temperature

# Distance Command Frame
cmd_d = [header_H, header_L, device_addr, data_length, get_dist_cmd]
cmd_d.append(sum(cmd_d) & 0xff)
cmd_d = bytes(cmd_d)

# Temperature Command Frame
cmd_t = [header_H, header_L, device_addr, data_length, get_temp_cmd]
cmd_t.append(sum(cmd_t) & 0xff)
cmd_t = bytes(cmd_t)

# Serial Port Configuration
ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 19200
ser.bytesize = 8
ser.partiy = 'N'
ser.stopbits = 1
ser.timeout = 5
#ser.write_timeout = 2
# Output Serial Port Configuration
print('Serial port data: ')
print(ser)

# Open Serial Port and check it's open
ser.open()
if ser.is_open:
    print('Serial port opened.')
else:
    print('Failed to open Serial Port. Exiting...')
    exit()

###############################################################################

def cleanup():
''' cleanup()
Description: Cleanup function closes serial port and exits.
'''
    print('')
    ser.close()
    if not ser.is_open:
        print('Serial port closed.')
    else:
        print('Failed to close Serial Port. Trying again')
        ser.close()
    exit()

def data_check(frame, len_frame):
''' data = data_check(frame, len_frame)
Description: Pass a frame of bytes and the expected frame length. Returns value
per command on success. Returns 998 on checksum failure and 999 with incomplete
* data.
'''
    if (len(frame) == len_frame): # Check for complete frame
        if ((sum(frame[0:-1]) & 0xff) == frame[-1]): # Check checksum
            return ((frame[-3]<<8) | frame[-2]) # Pass valid data
        else: # Checksum failed
            return 998
    else: # Data frame incomplete
        return 999

###############################################################################

last_dist_f = 0 # Initialize to zero

# Print header for data output
print('Distance (cm) | Temperature (C)')
c = 0
while c < 100:
    c += 1
    # Write Distance TX Command
    if (ser.write(cmd_d) != 6):
        print('Failed to write cmd_d.')
    time.sleep(0.01) # Sleep after writing
    # Read distance RX frame and check for valid data
    dist = data_check(ser.read(8), 8)
    dist_f = filter_coeff[0]*dist + filter_coeff[1]*last_dist_f # Filter
    last_dist_f = dist_f # Update values
    time.sleep(0.01) # Sleep after reading

    # Print Distance | Filtered
    print('\r{0:3} | {1:4.1f}'.format(dist, dist_f), end='')

    # Sleep for sample time
    time.sleep(sample_time)

# Cleanup
cleanup()
