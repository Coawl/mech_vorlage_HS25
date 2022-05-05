# Copyright 2020 Hochschule Luzern - Informatik
# Author: Peter Sollberger <peter.sollberger@hslu.ch>

from time import sleep, time
from gpiozero import DigitalInputDevice, LED, Button
from Encoder import Encoder
from Motor import Motor
from PIDController import PIDController
from Logger import Logger


# Predefine constants:
running = False          # Controller state
count = 0                # Interrupt counter
waitingtime = 1          # Waiting time in seconds for output

pidcontroller = PIDController()
logger = Logger(pidcontroller.kp, pidcontroller.ki, pidcontroller.kd, pidcontroller.refposition)
encoder = Encoder(23, 24)
motor = Motor('GPIO16', 'GPIO17', 'GPIO18')


def timerPinIRQ():
    """
    100 Hz timer for the regulator
    Method is activated with timer IRQ and should contain all actions necessary:
    1. Get current position
    2. Get current speed from PID controller
    3. Send current speed to Motor
    4. Save significant data for visualization.
    """
    global count

    count += 1          # Increase count
    # TODO: Führen Sie folgende Schritte aus, wenn der Motor laufen soll, also wenn 'running' True ist
    # 1. lesen Sie aus dem 'encoder'-Objekt die aktuelle Position aus
    # 2. berechnen Sie mit Hilfe des 'pidcontroller' die neue Geschwindigkeit
    # 3. setzen Sie auf dem Motor die errechnete Geschwindigkeit
    # zusätzlich geben Sie Position, Geschwindigkeit und die PIDactions über den Logger aus


def startPressed():
    """
    Start button pressed
    Clean data in Instances
    Turn on Motor
    set running=True
    """
    global running

    print("Starting")
    logger.clean()
    pidcontroller.reset()
    encoder.resetPosition()
    # TODO: Starten Sie den Motor

    running = True


def stopPressed():
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
        # TODO: Stopping Sie den Motor

        logger.showLoggings(feedback=True)
        running = False


if __name__ == '__main__':
    """
    Main loop outputs actual position, speed and IRQ count every second.
    """
    print("Starting main")

    # Define pins
    timerPin = DigitalInputDevice('GPIO25')
    startButton = Button('GPIO05')
    stopButton = Button('GPIO06')

    # Register ISR on input signals
    timerPin.when_activated = timerPinIRQ
    startButton.when_activated = startPressed
    stopButton.when_activated = stopPressed

    try:
        while True:
            """ 
            Endlessly do:
            get time, position and speed
            print position and speed
            wait until exactly one second has passed
            """
            now = time()
            pos = encoder.getPosition()
            v = motor.getSpeed()
            print("Position:", pos, "Speed: ", v)
            count = 0
            elapsed = time() - now
            sleep(waitingtime - elapsed)

    except KeyboardInterrupt:
        stopPressed()
        timerPin.close()
        motor.stop()
