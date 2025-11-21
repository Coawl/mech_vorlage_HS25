# Copyright 2020 Hochschule Luzern - Informatik
# Author: Peter Sollberger <peter.sollberger@hslu.ch>
# Modified for Raspberry Pi 5 compatibility

from gpiozero import LED
from spidev import SpiDev


class Motor:
    """
    Conveyor belt motor controller.
    """

    def __init__(self, direction_pin_nbr, brake_pin_nbr, stop_pin_nbr):
        """
        Initialize motor.
        :param direction_pin_nbr:
        :param brake_pin_nbr:
        :param stop_pin_nbr:
        """
        self.direction_pin = LED(direction_pin_nbr)
        self.brake_pin = LED(brake_pin_nbr)
        self.stop_pin = LED(stop_pin_nbr)

        self.spi = SpiDev()
        self.spi.open(0, 0)  # SPI0, CE0s
        self.spi.max_speed_hz = 4000000
        self.speed = 0.0

    def __analog_output(self, value):
        # low byte has 6 data bits
        # B7, B6, B5, B4, B3, B2, B1, B0
        # D5, D4, D3, D2, D1, D0,  X,  X
        low_byte = value << 2 & 0b11111100
        # high byte has control and 4 data bits
        # control bits are:
        # B7, B6,   B5, B4,     B3,  B2,  B1,  B0
        # W  ,BUF, !GA, !SHDN,  D9,  D8,  D7,  D6
        # B7=0:write to DAC, B6=0:unbuffered, B5=1:Gain=1X, B4=1:Output is active
        high_byte = ((value >> 6) & 0xff) | 0b0 << 7 | 0b0 << 6 | 0b1 << 5 | 0b1 << 4
        # by using spi.xfer2(), the CS is released after each block, transferring the
        # value to the output pin.
        self.spi.xfer2([high_byte, low_byte])

    def set_voltage(self, value):
        """
        Set the motor voltage in the range of -1023 to 1023. Higher values will be ignored.
        :param value: Voltage
        """
        if value >= 0:
            self.direction_pin.on()
        else:
            self.direction_pin.off()
            value = abs(value)
        if value > 1023:
            value = 1023
        self.speed = value
        self.__analog_output(value)

    def get_voltage(self):
        """
        Return actual voltage.
        """
        value = self.speed
        if self.direction_pin.value == 0:
            value *= -1
        return value

    def on(self):
        """
        Release brake and stop signal.
        """
        self.speed = 0
        self.__analog_output(0)
        self.stop_pin.on()
        self.brake_pin.on()

    def stop(self):
        """
        Immediately stop the motor using the stop and brake signal.
        """
        self.__analog_output(0)
        self.stop_pin.off()
        self.brake_pin.off()
        self.speed = 0

    def cleanup(self):
        """
        Clean up resources when done with motor.
        """
        self.stop()
        self.spi.close()
        self.direction_pin.close()
        self.brake_pin.close()
        self.stop_pin.close()
