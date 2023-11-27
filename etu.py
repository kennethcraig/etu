#!/usr/bin/env python3

import sys
import time
import datetime
import RPi.GPIO as gpio
from facetime import FaceTime

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

class ClockHands:

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


class Clock:
        handPos = FaceTime()
        handDriver = ClockHands()

        def __init__(self):
                self.loadHandTime()
                pass

        def save(self):
                """Saves in the format: minutes past 12:00 (0-719)"""
                with open("time.txt", "wt") as fp:
                        fp.write(str(self.handPos.getMinsPast12()))

        def load(self):
                try:
                        with open("time.txt", "rt") as fp:
                                self.handPos = FaceTime(int(fp.read()))
                except:
                        self.handPos = FaceTime(0)

        def moveOrWait(self, target: datetime.time):
                targetPos = FaceTime.fromTime(target)
                # Wait - if the target time is less than 70 minutes away.

        def moveForwardTo(self, target: datetime.time):
                targetFaceTime = FaceTime.fromTime(target)
                while targetFaceTime != self.handPos:
                        self.advanceHands()

        def advanceHands(self):
                self.handPos.advance()
                self.handDriver.advance()
                self.save()

def main(args):
        clock = Clock()
        
        hands = ClockHands()

        for i in range(0,100):
                hands.advance()
                


if __name__ == '__main__':
        sys.exit(main(sys.argv[1:]))