#!/usr/bin/env python3

from __future__ import annotations

import datetime

class FaceTime:
    """Represents the 720 minute cycle of an analogue clock face"""
    handPos = 0

    def __init__(self, minsPast12 : int = 0):
        """Constructor

        Args:
            minsPast12 (int, optional): The number of minutes past 12:00 on the clock face. Defaults to 0.
        """
        self.handPos = minsPast12 % 720

    def fromTime(set : datetime.time) -> FaceTime:
        """Constructs a FaceTime object from a datetime.time object

        Args:
            set (datetime.time): The datetime.time object to construct this from

        Returns:
            FaceTime: The newly constructed FaceTime
        """
        pos = (set.hour % 12) * 60 + set.minute
        return FaceTime(pos)

    def advance(self):
        """Advances the clock 1 minute
        """
        self.handPos = self.handPos + 1
        self.handPos = self.handPos % 720

    def getHandPos(self) -> int:
        """Returns the position of the clock in minutes past 12:00

        Returns:
            int: The position of the clock hands in minutes past 12:00
        """
        return self.handPos

    def __add__(self, rhs : FaceTime)-> FaceTime:
        """Adds two FaceTime objects

        Args:
            rhs (FaceTime): The FaceTime to add to this one

        Returns:
            FaceTime: The added FaceTime objects
        """
        return FaceTime(self.handPos + rhs.handPos)

    def __sub__(self, rhs : FaceTime) -> int:
        """Subtracts two FaceTime objects

        Args:
            rhs (FaceTime): The FaceTime object to subtract from this one

        Returns:
            int: The result of the subtraction in minutes (signed)
        """
        return self.handPos - rhs.handPos
    
    def __eq__(self, rhs) -> bool:
        return self.handPos == rhs.handPos
    
    def __ne__(self, rhs) -> bool:
        return self.handPos != rhs.handPos
    
    def __lt__(self, rhs):
        return self.handPos < rhs.handPos
    
    def __gt__(self, rhs):
        return self.handPos > rhs.handPos
    
    def __repr__(self) -> str:
        return f"FaceTime({self.handPos})"