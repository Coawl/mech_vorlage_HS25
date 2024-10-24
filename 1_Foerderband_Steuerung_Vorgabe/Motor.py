# Copyright 2020 Hochschule Luzern - Informatik
# Author: Peter Sollberger <peter.sollberger@hslu.ch>

from gpiozero import LED
from spidev import SpiDev


class Motor:
    """
    Conveyor belt motor controller.
    """
    def __init__(self, directionPinNbr, brakePinNbr, stopPinNbr):
        """
        Initialize motor.
        :param directionPinNbr:
        :param brakePinNbr:
        :param stopPinNbr:
        """
        self.directionPin = LED(directionPinNbr)
        self.brakePin = LED(brakePinNbr)
        self.stopPin = LED(stopPinNbr)

        self.spi = SpiDev()
        self.spi.open(0, 0)  # SPI0, CE0s
        self.spi.max_speed_hz = 4000000
        self.speed = 0.0

    def __analogOutput(self, value):
        # lowbyte has 6 data bits
        # B7, B6, B5, B4, B3, B2, B1, B0
        # D5, D4, D3, D2, D1, D0,  X,  X
        lowByte = value << 2 & 0b11111100
        # highbyte has control and 4 data bits
        # control bits are:
        # B7, B6,   B5, B4,     B3,  B2,  B1,  B0
        # W  ,BUF, !GA, !SHDN,  D9,  D8,  D7,  D6
        # B7=0:write to DAC, B6=0:unbuffered, B5=1:Gain=1X, B4=1:Output is active
        highByte = ((value >> 6) & 0xff) | 0b0 << 7 | 0b0 << 6 | 0b1 << 5 | 0b1 << 4
        # by using spi.xfer2(), the CS is released after each block, transferring the
        # value to the output pin.
        self.spi.xfer2([highByte, lowByte])

    def setSpeed(self, value):
        """
        Set the motor speed in the range of -1023 to 1023. Higher values will be ignored.
        :param value: Speed
        """
        if value >= 0:
            self.directionPin.on()
        else:
            self.directionPin.off()
            value = abs(value)
        if value > 1023:
            value = 1023
        self.speed = value
        self.__analogOutput(value)

    def getSpeed(self):
        """
        Return actual speed.
        """
        value = self.speed
        if self.directionPin.value == 0:
            value *= -1
        return value

    def on(self):
        """
        Release brake and stop signal.
        """
        self.speed = 0
        self.__analogOutput(0)
        self.stopPin.on()
        self.brakePin.on()

    def stop(self):
        """
        Immediately stop the motor using the stop and brake signal.
        """
        self.__analogOutput(0)
        self.stopPin.off()
        self.brakePin.off()
        self.speed = 0
