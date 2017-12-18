'''
* File: urm07_read_all.py
* Author: Parker Brown
* Date: 12/7/2017
* Course: MAE 198, Fall 2017
* Description: Script reads distance and temperature measurements from sensors
* at specified device address.
* Documentation for the sensors can be found here:
* https://www.dfrobot.com/wiki/index.php/URM07-UART_Ultrasonic_Sensor_SKU:_SEN0153
* URM07 sensors must be connected to the Raspberry Pi UART interface, header pins
* 8 (TX) and 10 (RX), and the 3.3V power supply; they can be daisy chained with
* unique device addresses.
'''

import serial
import time

sample_time = 0.05 # Sample Rate: 20 Hz

# Command Frame Header
header_H = 0x55 # Header High
header_L = 0xAA # Header Low
device_addr = [0x22, 0x33, 0x44] # Device addresses
data_length = 0x00 # Data length
get_dist_cmd = 0x02 # Command: Read Distance
get_temp_cmd = 0x03 # Command: Read Temperature

cmd_d = []
cmd_t = []
for dev in device_addr:
    # Distance Command Frame
    cmd1 = []
    cmd1 = [header_H, header_L, dev, data_length, get_dist_cmd]
    cmd1.append(sum(cmd1) & 0xff)
    cmd_d.append(bytes(cmd1))
    # Temperature Command Frame
    cmd2 = []
    cmd2 = [header_H, header_L, dev, data_length, get_temp_cmd]
    cmd2.append(sum(cmd2) & 0xff)
    cmd_t.append(bytes(cmd2))

# Serial Port Configuration
ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 19200
ser.bytesize = 8
ser.partiy = 'N'
ser.stopbits = 1
ser.timeout = 1
ser.write_timeout = 1
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

# Print header for data output
print('Device distances in (cm), temperature in (C).')
print('|     0x22    |     0x33    |     0x44    |')
print('| dist | temp | dist | temp | dist | temp |')
c = 0
dist = [0, 0, 0]
temp = [0.0, 0.0, 0.0]
while c < 100:
    c += 1
    # Iterate over devices
    for i in range(len(device_addr)):
            # Write Distance TX Command
        if (ser.write(cmd_d[i]) != 6):
            print('Failed to write cmd_d. Exiting...')
            cleanup()
        time.sleep(0.01) # Sleep after writing
        # Read distance RX frame and check for valid data
        dist[i] = data_check(ser.read(8), 8)
        time.sleep(0.01) # Sleep after reading

        # Write Temperature TX Command
        if c%5 == 0: # Only get temp every 5 iterations
            if (ser.write(cmd_t[i]) != 6):
                print('Failed to write cmd_t. Exiting...')
                cleanup()
            time.sleep(0.01) # Sleep after writing
            # Read Temperature RX Frame and check for valid data
            temp[i] = data_check(ser.read(8), 8)
            # Convert temp to cm
            if temp[i] != 998 and temp[i] != 999:
                temp[i] = 0.1 * temp[i]
            else:
                temp[i] = 0.0
            time.sleep(0.01) # Sleep after reading

    # Print Distance | Temperature
    print('\r| {0:4} | {1:4.1f} | {2:4} | {3:4.1f} | {4:4} | {5:4.1f} |'
    .format(dist[0],temp[0],dist[1],temp[1],dist[2],temp[2]), end='')

    # Sleep for sample time
    time.sleep(sample_time)

# Cleanup
cleanup()
