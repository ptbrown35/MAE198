import serial
import time

class urm07():
    def __init__(self):
        # Command Frame Header
        header_H = 0x55 # Header High
        header_L = 0xAA # Header Low
        self.device_addr = [0x22, 0x33, 0x44] # Device addresses
        data_length = 0x00 # Data length
        get_dist_cmd = 0x02 # Command: Read Distance

        self.cmd_d = []
        for dev in self.device_addr:
            # Distance Command Frame
            cmd = []
            cmd = [header_H, header_L, dev, data_length, get_dist_cmd]
            cmd.append(sum(cmd) & 0xff)
            self.cmd_d.append(bytes(cmd))

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
        dist = []
        for i in range(len(self.device_addr)):
            # Write Distance TX Command
            if (self.ser.write(self.cmd_d[i]) != 8):
                print('URM07: Failed to write cmd_d.')
            time.sleep(0.01) # Sleep after writing
            # Read distance RX frame and check for valid data
            dist[i] = data_check(self.ser.read(8), 8)
            time.sleep(0.01) # Sleep after reading
        return dist

    def shutdown(self):
        self.ser.close()
        if not self.ser.is_open:
            print('URM07: Serial port closed.')
        else:
            print('URM07: Failed to close Serial Port. Trying again...')
            self.ser.close()

################################################################################

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
