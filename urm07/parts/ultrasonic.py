import serial
import time

''' data = data_check(frame, len_frame)
Description: Pass a frame of bytes and the expected frame length. Returns value
per command on success. Returns NaN on failure.
'''
def data_check(frame, len_frame):
    #print('data_check checking data!')
    if (len(frame) == len_frame): # Check for complete frame
        if ((sum(frame[0:-1]) & 0xff) == frame[-1]): # Check checksum
            return ((frame[-3]<<8) | frame[-2]) # Pass valid data
        else: # Checksum failed
            return '998'
    else: # Data frame incomplete
        return '999'

class ultrasonic:

    def __init__(self):
        # Command Frame Header
        header_H = 0x55 # Header High
        header_L = 0xAA # Header Low
        self.device_addr = [0x44, 0x33, 0x22] # Device addresses: Left to Right
        data_length = 0x00 # Data length
        get_dist_cmd = 0x02 # Command: Read Distance

        self.cmd_d = []
        for dev in self.device_addr:
            # Distance Command Frame
            cmd = []
            cmd = [header_H, header_L, dev, data_length, get_dist_cmd]
            cmd.append(sum(cmd) & 0xff)
            self.cmd_d.append(bytes(cmd))

        # Filter coefficients
        self.filter_coeff = [0.6, 0.4]
        self.dist = [0, 0, 0]
        self.dist_f = [0, 0, 0]
        self.last_dist_f = [0, 0, 0]

        # Serial Port Configuration
        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyS0'
        self.ser.baudrate = 19200
        self.ser.bytesize = 8
        self.ser.partiy = 'N'
        self.ser.stopbits = 1
        self.ser.timeout = 5

        # Open Serial Port and check it's open
        self.ser.open()
        if self.ser.is_open:
            print('URM07: Serial port opened.')
        else:
            print('URM07: Failed to open Serial Port.')

    def run(self):
        for i in range(len(self.device_addr)):
            # Write Distance TX Command
            if (self.ser.write(self.cmd_d[i]) != 6):
                print('URM07: Failed to write cmd_d.')
            time.sleep(0.01) # Sleep after writing
            # Read distance RX frame and check for valid data
            self.dist[i] = data_check(self.ser.read(8), 8)
            # Filtering
            self.dist_f[i] = self.filter_coeff[0] * self.dist[i] + self.filter_coeff[1] * self.last_dist_f[i]
            self.last_dist_f[i] = self.dist_f[i]

            time.sleep(0.01) # Sleep after reading
        print('{0:5.1f} {1:5.1f} {2:5.1f}'.format(self.dist_f[0], self.dist_f[1], self.dist_f[2]))
        # print('{0:3} {1:5.3f} {2:5.3f}'.format(self.dist[0], self.last_dist_f[0], self.dist_f[0]))
        return self.dist_f

    def shutdown(self):
        print('Shutting down URM07')
        self.ser.close()
        if not self.ser.is_open:
            print('URM07: Serial port closed.')
        else:
            print('URM07: Failed to close Serial Port. Trying again...')
            self.ser.close()
