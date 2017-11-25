import sys
import serial
import time


sleep_time = 0.05

header_H = 0x55 #Header
header_L = 0xAA #Header
device_Addr = 0x11 #Address
data_Length = 0x00 #Data length
get_Dis_CMD = 0x02 #Command: Read Distance
checksum = 0x12 #checksum

frame_tx = bytearray([header_H, header_L, device_Addr, data_Length, get_Dis_CMD, checksum])

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

#ser.write(frame_tx)
#print('TX Frame: ' + str(frame_tx))

#frame_rx = ser.read(8)
#print('RX Frame: ' + str(frame_rx))
#print('Distance: ' + str(frame_rx[6]) + ' cm')
#time.sleep(1)

print('Distance (cm)')
print('')
c = 0
while c < 50:
    c += 1
    ser.write(frame_tx)
    frame_rx = ser.read(8)
    #print(str(frame_tx) + '\t' + str(frame_rx) + '\t' + str(frame_rx[6]))
    #sys.stdout.write('{0}\r'.format(frame_rx[6]))
    #sys.stdout.flush()
    print(frame_rx[6])
    time.sleep(sleep_time)

ser.close()
print('Serial port closed: ' + str(not ser.is_open))
