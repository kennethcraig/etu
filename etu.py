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

class Clock:

        r0 = Relay(0)
        r1 = Relay(1)
        lastPolarityPositive = False

        def __init__(self) -> None:
                self.r0.close()
                self.r1.close()

        def advance(self):
                if self.lastPolarityPositive:
                        self.r0.open()
                        self.r1.close()
                else:
                        self.r0.close()
                        self.r1.open()

                self.lastPolarityPositive = not self.lastPolarityPositive

                #40ms dwell
                time.sleep(0.2)
                self.r0.close()
                self.r1.close()

def main(args):
        clock = Clock()
        while True:
                clock.advance()
                


if __name__ == '__main__':
        sys.exit(main(sys.argv[1:]))