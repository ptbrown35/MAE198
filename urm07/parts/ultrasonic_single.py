import sys
import serial
import time

class ultrasonic:

    def __init__(self):

        self.dataArray = [1,2,3]

        sleep_time = 0.05

        header_H = 0x55 #Header
        header_L = 0xAA #Header
        device_Addr = 0x22 #Address
        data_Length = 0x00 #Data length
        get_Dis_CMD = 0x02 #Command: Read Distance

        self.frame_tx = [header_H, header_L, device_Addr, data_Length, get_Dis_CMD]
        self.frame_tx.append(sum(self.frame_x) & 0xff)
        self.frame_tx = bytes(self.frame_tx)

        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyS0'
        self.ser.baudrate = 19200
        self.ser.bytesize = 8
        self.ser.partiy = 'N'
        self.ser.stopbits = 1
        self.ser.timeout = 5
        #ser.write_timeout = 2
        self.ser.open()
#        print('Serial port data: ')
#        print(ser)
        print("Adding ultrasonic")

    def update(self):

        self.ser.write(self.frame_tx)
        self.frame_rx = ser.read(8)
        print(self.frame_rx[6])
        time.sleep(sleep_time)
        self.dataArray = frame_rx[6]
        #if not self.on:
         #   break
    def shutdown(self):

        self.on = False
        print ("stopping ultSensors")
        ser.close()
        print('Serial port closed: ' + str(not ser.is_open))

    def run(self):
        self.ser.write(self.frame_tx)
        self.frame_rx = self.ser.read(8)
        #print(self.frame_rx[6])
        #time.sleep(sleep_time)
        self.dataArray = [self.frame_rx[6], self.frame_rx[6], self.frame_rx[6]]
        print(self.dataArray)
        #print(frame_rx[6])
        return self.dataArray
