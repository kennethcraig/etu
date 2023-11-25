#!/usr/bin/env python3

import sys
import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

class Relay:
        pins = [15, 29]

        def __init__(self, pin):
                self.pin = self.pins[pin]
                gpio.setup(self.pin, gpio.OUT)
                gpio.output(self.pin, gpio.LOW)

        def open(self):
                gpio.output(self.pin, gpio.HIGH)

        def close(self):
                gpio.output(self.pin, gpio.LOW)



def main(args):
        r0 = Relay(0)
        r1 = Relay(1)


        while True:
                r0.open()
                r1.close()
                time.sleep(0.001)
                r0.close()
                r1.open()
                time.sleep(0.001)


if __name__ == '__main__':
        sys.exit(main(sys.argv[1:]))