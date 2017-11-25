import serial
import time


header_H = 0x55 #Header
header_L = 0xAA #Header
device_Addr = 0xAB #Address
data_Length = 0x01 #Data length
set_Addr_CMD = 0x55 #Command: Set Device Address
device_Addr_new = 0x22 #New Address: 0x22
checksum = 0x22 #Distance checksum

cmd = bytearray([header_H, header_L, device_Addr, data_Length, set_Addr_CMD, device_Addr_new, checksum])

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

print('Setting Address to 0x22...')

print('Command: ' + str(cmd))
ser.write(cmd)
time.sleep(0.1)

rx = ser.read(7)
time.sleep(0.1)
print('Received: ' + str(rx))
print('2nd to last byte: 0xCC if successful, 0xEE if failed')

ser.close()
print('Serial port closed: ' + str(not ser.is_open))
