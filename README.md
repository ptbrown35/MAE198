# MAE198
## Description
This repository contains code for interfacing a Raspberry Pi with the cheap COTS ultrasonic sensors [URM07](https://www.dfrobot.com/wiki/index.php/URM07-UART_Ultrasonic_Sensor_SKU:_SEN0153). The provided scripts communicate with the sensors to read distance and temperature data and set device addresses and baud rates for the sensor modules. With unique device addresses, the sensors can be daisy chained together over their shared UART serial bus. There is also a script provided that can be integrated as a part into the [donkeyar](http://docs.donkeycar.com/) code base.
## scripts
#### urm07_read.py
Script reads distance and temperature measurements from sensor at specified device address.
#### urm07_read_all.py
Script reads distance and temperature measurements from sensors at specified device address.
#### urm07_read_filtered.py
Script reads distance measurements from sensor at specified device address and applies a first order low pass filter to the raw data.
#### urm07_set_address.py
Script sets unique device address.
#### urm07_set_baudrate.py
Script sets device baud rate.
#### ultrasonic.py
Script is a "part" for the [donkeyar](http://docs.donkeycar.com/) code base, returning filtered distance data to the autopilot.
## Hardware
Documentation for the sensors can be found [here](https://www.dfrobot.com/wiki/index.php/URM07-UART_Ultrasonic_Sensor_SKU:_SEN0153).
URM07 sensors must be connected to the Raspberry Pi UART interface, header pins 8 (TX) and 10 (RX), and the 3.3V power supply; they can be daisy chained with unique device addresses.
