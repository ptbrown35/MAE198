'''
* File: urm07_set_baudrate.py
* Author: Parker Brown
* Date: 12/7/2017
* Course: MAE 198, Fall 2017
* Description: Script sets device baud rate.
* Documentation for the sensors can be found here:
* https://www.dfrobot.com/wiki/index.php/URM07-UART_Ultrasonic_Sensor_SKU:_SEN0153
* URM07 sensors must be connected to the Raspberry Pi UART interface, header pins
* 8 (TX) and 10 (RX), and the 3.3V power supply.
'''

import serial
import time

header_H = 0x55 # Header High
header_L = 0xAA # Header Low
device_addr = 0xAB # Address: Generic
data_length = 0x01 # Data length
set_baud_cmd = 0x08 # Command: Set Device Baudrate
baud_new = 0x08 # New Baudrate: 57600

cmd = [header_H, header_L, device_addr, data_length, set_baud_cmd, baud_new]
cmd.append(sum(cmd_d) & 0xff)
cmd = bytes(cmd_d)

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

print('Setting Baudrate to 57600...')

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
