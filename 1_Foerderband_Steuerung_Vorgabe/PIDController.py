# Copyright 2020 Hochschule Luzern - Informatik
# Author: Simon van Hemert <simon.vanhemert@hslu.ch>
# Author: Peter Sollberger <peter.sollberger@hslu.ch>

class PIDController:
    """
    Implements a PID controller.
    """
    def __init__(self):
        """
        Save relevant constants to self
        """
        # Predefine constants and set variables:
        self.refposition = 415               # Reference position in mm
        self.errorLinear = self.refposition  # Initial error
        self.errorIntegral = 0

        # PID constants:
        self.kp = 0.5
        self.ki = 0.05
        self.kd = 0.005

    def reset(self):
        """
        Restore controller with initial values.
        """
        self.errorLinear = self.refposition
        self.errorIntegral = 0

    def calculateTargetValue(self, actualValue):
        """
        Calculate next target values with the help of a PID controller.
        """
        # TODO:
        # 1. Berechnen Sie
        #    - den aktuellen Positions-Fehler 'errorLinear'
        #    - das aktuelle Fehler-Integral 'errorIntegral'; denken
        #      Sie dabei an windup
        #    - das aktuelle Fehler-Derivative 'errorDerivative'
        # 2. Berechnen Sie aus den Fehlern die P, I und D-Anteile;
        #    Sie können diese Werte in den Variablen p_part, i_part
        #    und d_part abspeichern oder die Berechnungen direkt in die
        #    Liste der PIDactions schreiben

        # Save the three parts of the controller in a vector
        PIDactions = [p_part, i_part, d_part]
        # The output speed is the sum of the parts
        targetValue = sum(PIDactions)

        return int(targetValue), PIDactions
