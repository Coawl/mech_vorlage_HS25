# Copyright 2020 Hochschule Luzern - Informatik
# Author: Peter Sollberger <peter.sollberger@hslu.ch>
# Modified for Raspberry Pi 5 compatibility

import select
import sys
from time import sleep, time
from gpiozero import DigitalInputDevice, Button

from Encoder import Encoder
from Motor import Motor
from PIDControllerVelocity import PIDControllerVelocity
from LoggerVelocity import LoggerVelocity

# Global variables
running = False  # Controller state
waiting_time = 1  # Waiting time in seconds for output

# Objects - using BCM GPIO numbering (plain integers)
pidcontroller = PIDControllerVelocity()
logger = LoggerVelocity(pidcontroller.kp, pidcontroller.Tn, pidcontroller.Tv, pidcontroller.reference_value)
encoder = Encoder(23, 24)
motor = Motor(16, 17, 18)  # Changed from 'GPIO16' to 16, etc.

# Variables for velocity calculation
last_position = 0
last_time = 0
filtered_velocity = 0
velocity_filter_alpha = 0.3  # Low-pass filter coefficient (0-1, smaller = smoother)


def timer_pin_irq():
    """
    100 Hz timer for the regulator
    Method is activated with timer IRQ and should contain all actions
    necessary:
    1. Get current velocity
    2. Get voltage from PID controller
    3. Send voltage to Motor
    4. Save significant data for visualization.
    """
    global last_position, last_time, filtered_velocity
    
    if running:
        current_position = encoder.get_position()
        current_time = time()
        
        # Calculate velocity (mm/s) with 0.01s fixed time interval
        if last_time > 0:
            dt = 0.01  # Fixed 100 Hz timer interval
            current_velocity = (current_position - last_position) / dt
            
            # Apply low-pass filter to smooth velocity
            filtered_velocity = velocity_filter_alpha * current_velocity + (1 - velocity_filter_alpha) * filtered_velocity
        else:
            filtered_velocity = 0
        
        last_position = current_position
        last_time = current_time
        
        motor_voltage, pid_actions = pidcontroller.calculate_controller_output(filtered_velocity)
        motor.set_voltage(motor_voltage)
        logger.log(filtered_velocity, motor_voltage, pid_actions)


def start_pressed():
    """
    Start button pressed
    Clean data in Instances
    Turn on Motor
    set running=True
    """
    global running, last_position, last_time, filtered_velocity

    print("Starting")
    logger.clean()
    pidcontroller.reset()
    encoder.reset_position()
    last_position = 0
    last_time = 0
    filtered_velocity = 0
    motor.on()

    running = True


def stop_pressed():
    """
    Stop button pressed
    when running was True:
    set running=False
    stop Motor
    create figures
    """
    global running

    if running:
        print("Stopping")
        motor.stop()

        logger.showLoggings(feedback=True, save=True)
        running = False


def cleanup():
    """
    Clean up all resources
    """
    global timerPin, startButton, stopButton, motor, encoder

    print("Cleaning up...")
    motor.cleanup()
    encoder.cleanup()
    timerPin.close()
    startButton.close()
    stopButton.close()


if __name__ == '__main__':
    """
    Main loop outputs actual position and speed every second.
    """
    print("Starting main")

    # Define pins
    timerPin = DigitalInputDevice(25)
    startButton = Button(5)
    stopButton = Button(6)

    # Register ISR on input signals
    timerPin.when_activated = timer_pin_irq
    startButton.when_activated = start_pressed
    stopButton.when_activated = stop_pressed

    try:
        # Dieser Teil des Programms ist nur für die Ausgabe der aktuellen
        # Position und Geschwindigkeit zuständig. Die eigentliche Regelung
        # geschieht mit der Funktion timerPinIRQ()
        while True:
            """
            Endlessly do:
            get time, position and speed
            print position and speed
            wait until exactly one second has passed
            """
            now = time()
            pos = encoder.get_position()
            v = motor.get_voltage()
            print("Position [mm]:", pos, "Voltage [%]: ", v * 100 / 1023)

            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline().strip()

                if line == "s":
                    print("Tastatur: Start gedrückt (s)")
                    start_pressed()  # gleiche Funktion wie Button

                elif line == "q":
                    print("Tastatur: Stop/Beenden gedrückt (q)")
                    stop_pressed()  # Motor/Regelung stoppen

            elapsed = time() - now
            sleep(max(0.0, waiting_time - elapsed))

    except KeyboardInterrupt:
        stop_pressed()
        timerPin.close()
        cleanup()
