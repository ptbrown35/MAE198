# test serial GPIOs, TX (10), RX (12)


import RPi.GPIO as GPIO

RX = 10
TX = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TX, GPIO.OUT)
GPIO.setup(RX, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

print(GPIO.input(RX))

#GPIO.output(TX, GPIO.HIGH)

GPIO.cleanup()
