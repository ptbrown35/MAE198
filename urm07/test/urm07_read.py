import sys
import serial
import time

sample_time = 0.05

# Command Frame Header
header_H = 0x55 #Header
header_L = 0xAA #Header

# Device Addresses
device_Addr = 0xAB #Address: Generic
#device_Addr = 0x22 #Address: 0x22
#device_Addr = 0x33 #Address: 0x33
#device_Addr = 0x44 #Address: 0x44

data_Length = 0x00 #Data length
get_Dis_CMD = 0x02 #Command: Read Distance
get_Temp_CMD = 0x03 #Command: Read Temperature

checksum_d = 0xAC #Distance checksum: 0xAB
#checksum_d = 0x23 #Distance checksum: 0x22
#checksum_d = 0x34 #Distance checksum: 0x33
#checksum_d = 0x45 #Distance checksum: 0x44

checksum_t = 0xAD #Temperature checksum: 0xAB
#checksum_t = 0x24 #Temperature checksum: 0x22
#checksum_t = 0x35 #Temperature checksum: 0x33
#checksum_t = 0x46 #Temperature checksum: 0x44

# Distance Command Frame
cmd_d = bytearray([header_H, header_L, device_Addr, data_Length, get_Dis_CMD, checksum_d])
# Temperature Command Frame
cmd_t = bytearray([header_H, header_L, device_Addr, data_Length, get_Temp_CMD, checksum_t])

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
print()


if ser.open():
    print('Serial port open: ' + str(ser.is_open))
else:
    print('Failed to open Serial Port. Exiting...')
    exit()

print('Distance (cm) | Temperature (C)')
c = 0
while c < 50:
    c += 1
    ser.write(cmd_d)
    time.sleep(0.01)
    rx_d = ser.read(8)
    time.sleep(0.01)
    ser.write(cmd_t)
    time.sleep(0.01)
    rx_t = ser.read(8)
    print(str(rx_d[6]) + ' | ' + str(0.1*rx_t[6]))
    time.sleep(sample_time)

ser.close()
print('Serial port closed: ' + str(not ser.is_open))
