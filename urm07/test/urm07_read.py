import sys
import serial
import time

sample_time = 0.05

header_H = 0x55 #Header
header_L = 0xAA #Header


device_Addr = 0xAB #Address
#device_Addr = 0x22 #Address
#device_Addr = 0x33 #Address
#device_Addr = 0x44 #Address

data_Length = 0x00 #Data length
get_Dis_CMD = 0x02 #Command: Read Distance
get_Temp_CMD = 0x03 #Command: Read Temperature

checksum_d = 0xAC #Distance checksum
#checksum_d = 0x23 #Distance checksum
#checksum_d = 0x34 #Distance checksum
#checksum_d = 0x45 #Distance checksum

checksum_t = 0xAD #Temperature checksum
#checksum_t = 0x24 #Temperature checksum
#checksum_t = 0x35 #Temperature checksum
#checksum_t = 0x46 #Temperature checksum

cmd_d = bytearray([header_H, header_L, device_Addr, data_Length, get_Dis_CMD, checksum_d])

cmd_t = bytearray([header_H, header_L, device_Addr, data_Length, get_Temp_CMD, checksum_t])

ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 19200
ser.bytesize = 8
ser.partiy = 'N'
ser.stopbits = 1
ser.timeout = 5
#ser.write_timeout = 2
print('Serial port data: ')
print(ser)
print()

ser.open()
print('Serial port open: ' + str(ser.is_open))

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
