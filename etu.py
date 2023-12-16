#!/usr/bin/env python3

from __future__ import annotations

import sys
import time
import datetime
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

try:
        import RPi.GPIO as gpio
except:
        class gpio:
                BOARD="Board"
                OUT="Out"
                LOW="Low"
                HIGH="High"
                def setup(pin, dir):
                        logging.debug(f"gpio.setup({pin}, {dir})")
                        
                def output(pin, dir):
                        logging.debug(f"gpio.output({pin}, {dir})")
                        
                def setmode(mode):
                        logging.debug(f"gpio.setmode({mode})")
                        
                def setwarnings(warnings):
                        logging.debug(f"gpio.setwarnings({warnings})")
                        

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
                logging.info("ClockHands.advance()")
                if self.lastPolarityPositive:
                        self.r0.open()
                        self.r1.close()
                else:
                        self.r0.close()
                        self.r1.open()

                self.lastPolarityPositive = not self.lastPolarityPositive

                #40ms dwell
                time.sleep(0.04)
                self.r0.close()
                self.r1.close()
                time.sleep(0.04)


class Clock:
        handPos = FaceTime()
        handDriver = ClockHands()

        def __enter__(self):
                self.load()
                return self

        def __exit__(self, exc_type, exc_value, traceback):
                self.save()

        def save(self):
                """Saves in the format: minutes past 12:00 (0-719)"""
                with open("time.txt", "wt") as fp:
                        fp.write(str(self.handPos.getHandPos()))
                logging.info(f"Clock.save() - saved clock with {self.handPos.getHandPos()}")
                

        def load(self):
                try:
                        with open("time.txt", "rt") as fp:
                                self.handPos = FaceTime(int(fp.read()))
                        logging.info(f"Clock.load() - loaded clock with {self.handPos.getHandPos()}")
                except Exception as e:
                        self.handPos = FaceTime(0)
                        logging.info(f"Clock.load() failed. default to 0")
                        logging.info(e)


        def moveOrWait(self, target: datetime.time):
                targetPos = FaceTime.fromTime(target)
                diff = self.handPos - targetPos
                if diff < 0 or diff > 90:
                        self.moveForwardTo(target)
                # otherwise, do nothing, eventually we'll reach that time

        def moveForwardTo(self, target: datetime.time):
                targetFaceTime = FaceTime.fromTime(target)
                logging.debug(f"Clock.moveForwardTo({target}) - moving to {targetFaceTime}")
                while targetFaceTime != self.handPos:
                        self.advanceHands()


        def advanceHands(self):
                logging.info("Clock.advanceHands()")
                self.handPos.advance()
                self.handDriver.advance()
                self.save()


def main(args):
        if len(args) and args[0] == "--test":
                hands = ClockHands()
                for i in range(0, 10):
                        hands.advance()
                return 
        with Clock() as clock:
                while True:
                        clock.moveOrWait(datetime.datetime.now())
                        time.sleep(1)
                


if __name__ == '__main__':
        sys.exit(main(sys.argv[1:]))