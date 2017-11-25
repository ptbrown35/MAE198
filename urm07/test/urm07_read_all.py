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
print('Device distances in (cm), temperature in (C).')
print('|     0x22    |     0x33    |     0x44    |')
print('| dist | temp | dist | temp | dist | temp |')
c = 0
dist = []
temp = []
while c < 100:
    c += 1
    # Iterate over devices
    for i in range(len(device_addr)):
        # Write Distance TX Command
        if (ser.write(cmd_d[i]) != 8):
            print('Failed to write cmd_d. Exiting...')
            cleanup()
        time.sleep(0.01) # Sleep after writing
        # Read distance RX frame and check for valid data
        dist[i] = data_check(ser.read(8), 8)
        time.sleep(0.01) # Sleep after reading

        # Write Temperature TX Command
        if (ser.write(cmd_t[i]) != 8):
            print('Failed to write cmd_t. Exiting...')
            cleanup()
        time.sleep(0.01) # Sleep after writing
        # Read Temperature RX Frame and check for valid data
        temp[i] = data_check(ser.read(8), 8)
        # Convert temp to cm
        if temp[i] != 'NaN':
            temp[i] = 0.1 * temp[i]

    # Print Distance | Temperature
    print('\r| {0:4} | {1:4} | {2:4} | {3:4} | {4:4} | {5:4} |'
    .format(dist[0],dist[1],dist[2],temp[0],temp[1],temp[2]), end='')

    # Sleep for sample time
    time.sleep(sample_time)

cleanup()

###############################################################################

''' cleanup()
Description: Cleanup function closes serial port and exits.
'''
def cleanup():
    print('')
    ser.close()
    if not ser.is_open:
        print('Serial port closed.')
    else:
        print('Failed to close Serial Port. Trying again')
        ser.close()
    exit()

''' data = data_check(frame, len_frame)
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