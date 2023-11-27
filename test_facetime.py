#!/usr/bin/env python3

from facetime import FaceTime
from datetime import time
import unittest

class TestFacetime(unittest.TestCase):

    def test_construct(self):
        ft = FaceTime()
        self.assertEqual(ft.handPos, 0)


    def test_paramConstruct(self):
        ft = FaceTime(123)
        self.assertEqual(ft.handPos, 123)


    def test_paramConstructWrap(self):
        ft = FaceTime(726)
        self.assertEqual(ft.handPos, 6)


    def test_advance(self):
        ft = FaceTime()
        ft.advance()
        self.assertEqual(ft.handPos, 1)
        ft.advance()
        self.assertEqual(ft.handPos, 2)


    def test_advanceWrap(self):
        ft = FaceTime(718)
        ft.advance()
        self.assertEqual(ft.handPos, 719)
        ft.advance()
        self.assertEqual(ft.handPos, 0)
        ft.advance()
        self.assertEqual(ft.handPos, 1)

    def test_fromTime(self):
        ft = FaceTime.fromTime(time(0,0,0))
        self.assertEqual(ft.handPos, 0)

        ft = FaceTime.fromTime(time(1, 0, 0))
        self.assertEqual(ft.handPos, 60)

        ft = FaceTime.fromTime(time(1,30, 0))
        self.assertEqual(ft.handPos, 90)

        ft = FaceTime.fromTime(time(14, 0, 0))
        self.assertEqual(ft.handPos, 120)


    def test_accessor(self):
        ft = FaceTime(123)
        self.assertEqual(ft.getHandPos(), 123)


    def test_add(self):
        a = FaceTime(30)
        b = FaceTime(60)
        c = FaceTime(718)

        self.assertEqual((a + b).getHandPos(), 90)
        self.assertEqual((a + c).getHandPos(), 28)
        

    def test_sub(self):
        a = FaceTime(30)
        b = FaceTime(20)
        c = FaceTime(719)

        self.assertEqual((a - b).getHandPos(), 10)
        self.assertEqual((b - a).getHandPos(), 710)