import serial
import time


header_H = 0x55 # Header High
header_L = 0xAA # Header Low
device_addr = 0x11 # Address: Generic
data_length = 0x01 # Data length
set_addr_cmd = 0x55 # Command: Set Device Address
device_addr_new = 0x44 # New Address: 0x22

cmd = [header_H, header_L, device_addr, data_length, set_addr_cmd, device_addr_new]
cmd.append(sum(cmd) & 0xff)
cmd = bytes(cmd)

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
exit()
