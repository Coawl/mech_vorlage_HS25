# Copyright 2022 Hochschule Luzern - Informatik
# Author: Silvan Wegmann <silvan.wegmann@hslu.ch>
import unittest
import RPi.GPIO as GPIO
from Encoder import Encoder


class EncoderTest(unittest.TestCase):
    def setUp(self):
        self.uut = Encoder(23, 24)

    def test_run_one_circumference(self):
        # With 4 edges per tic and 1024 tics per rotation, we
        # should get the full Pi*Radius = 3.14152 * 58mm = 182mm
        # of position change which equals one circumference
        # of the wheel
        for i in range(4*1024):
            GPIO.next_edge_on_encoder(self.uut)
        self.assertEqual(self.uut.getPosition(), 182)

    def test_same_distance_forward_and_backward(self):
        for i in range(512):
            GPIO.next_edge_on_encoder(self.uut, "forward")
        for i in range(512):
            GPIO.next_edge_on_encoder(self.uut, "backward")
        self.assertEqual(self.uut.getPosition(), 0)
