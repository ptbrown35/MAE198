import serial
import time

sample_time = 0.05 # Sample Rate: 20 Hz

# Command Frame Header
header_H = 0x55 # Header High
header_L = 0xAA # Header Low

# Device Addresses
device_addr = 0xAB # Address: Generic
#device_addr = 0x22 # Address: 0x22
#device_addr = 0x33 # Address: 0x33
#device_addr = 0x44 # Address: 0x44

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

# Print header for data output
print('Distance (cm) | Temperature (C)')
c = 0
while c < 100:
    c += 1

    # Write Distance TX Command
    if (ser.write(cmd_d) != 8):
        print('Failed to write cmd_d.')
    time.sleep(0.01) # Sleep after writing
    # Read distance RX frame and check for valid data
    dist = data_check(ser.read(8), 8)
    time.sleep(0.01) # Sleep after reading

    # Write Temperature TX Command
    if (ser.write(cmd_t) != 8):
        print('Failed to write cmd_t.')
    time.sleep(0.01) # Sleep after writing
    # Read Temperature RX Frame and check for valid data
    temp = data_check(ser.read(8), 8)
    # Convert temp to cm
    if temp != 'NaN':
        temp = 0.1 * temp

    # Print Distance | Temperature
    print('\r{0:3} | {1:4}'.format(dist, temp), end='')

    # Sleep for sample time
    time.sleep(sample_time)

print('')

# Cleanup
ser.close()
if not ser.is_open:
    print('Serial port closed.')
else:
    print('Failed to close Serial Port. Trying again')
    ser.close()

''' data_check(frame, len_frame)
Description: Pass a frame of bytes and the expected frame length. Returns value
per command on success. Returns NaN on failure.
'''
def data_check(frame, len_frame):
    if (len(frame) == len_frame): # Check for complete frame
        if ((sum(frame[0:-1]) & 0xff) == frame[-1]): # Check checksum
            return ((frame[-3]<<8) | frame[-2]) # Pass valid data
        else: # Checksum failed
            return 'NaN'
    else: # Data frame incomplete
        return 'NaN'
