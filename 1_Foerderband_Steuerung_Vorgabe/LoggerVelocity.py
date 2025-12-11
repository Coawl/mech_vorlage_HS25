# Copyright 2020 Hochschule Luzern - Informatik
# Author: Simon van Hemert <simon.vanhemert@hslu.ch>
# Author: Peter Sollberger <peter.sollberger@hslu.ch>
# Modified for velocity control logging

from matplotlib import pyplot as plt
from array import array
from multiprocessing import Process
import sys
import numpy as np


class LoggerVelocity:
    """"
     Logs current velocity and current voltage and on request visualizes collected values concurrently
    """

    def __init__(self, kp, ki, kd, reference_value):
        """
        Create a logger and save parameters for displaying.
        """
        self.__title = "Kp = " + str(round(kp, 3)) + " Tn = " + str(round(ki, 3)) + " Tv = " + str(round(kd, 3)) \
                       + " Refvel = " + str(round(reference_value, 1)) + " mm/s"
        self.__outputs = array('l')
        self.__velocities = array('f')
        self.__Paction = array('f')
        self.__Iaction = array('f')
        self.__Daction = array('f')
        self.refvel = reference_value

    def clean(self):
        """
        Remove all previously stored values.
        """
        del self.__velocities
        del self.__outputs
        del self.__Paction
        del self.__Iaction
        del self.__Daction

        self.__outputs = array('l')
        self.__velocities = array('f')
        self.__Paction = array('f')
        self.__Iaction = array('f')
        self.__Daction = array('f')

    def log(self, velocity, output, PIDactions):
        """
        Add a data tuple to the log.
        """
        self.__velocities.append(velocity)
        self.__outputs.append(output)
        self.__Paction.append(PIDactions[0])
        self.__Iaction.append(PIDactions[1])
        self.__Daction.append(PIDactions[2])

    def showLoggings(self, feedback=False, save=False):
        """
        Display a graph of the recorded values.
        """
        t = Process(target=self.displayPlot, args=(self.__velocities.tolist(), self.__outputs.tolist(), self.__title,
                                                   [self.__Paction, self.__Iaction, self.__Daction],
                                                   feedback, self.refvel, save))
        t.start()

    @staticmethod
    def displayPlot(velocities, outputs, title, PIDactionsCopy, feedback, refvel, save):
        """
        Thread function to display values with the help of matplotlib.
        Plots Velocity and output voltage over time. Optionally the Feedback-actions can be plotted.
        figures and data are saved to png and .txt when save=True
        """
        try:
            time_ax = np.arange(len(velocities)) * 0.01

            # Calculate constants for velocity control
            # Overshoot
            max_vel = np.max(velocities)
            min_vel = np.min(velocities)
            overshoot = max_vel - refvel if refvel > 0 else refvel - min_vel

            # Rise time --> time between 10% and 90%
            bandmin = 0.1 * refvel
            bandmax = 0.9 * refvel
            # Find times
            try:
                risetime = np.interp([bandmin, bandmax], velocities, time_ax)
                risetime = np.round(risetime[1] - risetime[0], 3)
            except:
                risetime = 0
                
            # Clamp output voltages
            for i in range(len(outputs)):
                if abs(outputs[i]) > 1024:
                    if outputs[i] > 0:
                        outputs[i] = 1024
                    else:
                        outputs[i] = -1024

            # Settle time 5%
            bandmin = 0.95 * refvel
            bandmax = 1.05 * refvel
            settletime = time_ax[-1]  # default to last time
            # Find indices where outside band
            for i in range(len(velocities)):
                if velocities[i] > bandmax or velocities[i] < bandmin:
                    settletime = time_ax[i]

            settletime = np.round(settletime, 3)

            # Create figure for Velocity and output voltage
            fig = plt.figure(figsize=(12, 5))
            ax1 = fig.add_subplot(121)
            color = 'tab:red'
            ax1.set_xlabel('Time (0.01s)')
            ax1.set_ylabel('Velocity [mm/s]', color=color)
            ax1.plot(velocities, color=color)
            ax1.title.set_text('Velocity and Output Voltage')
            plt.axhline(refvel, alpha=0.5, color="grey", label="Setpoint")
            plt.axhline(bandmin, alpha=0.5, color="grey", linestyle=":")
            plt.axhline(bandmax, alpha=0.5, color="grey", linestyle=":")
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.legend(loc='upper left')

            ax12 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'tab:blue'
            ax12.set_ylabel('Output Voltage [DAC units]', color=color)
            ax12.plot(outputs, color=color)
            ax12.tick_params(axis='y', labelcolor=color)

            if feedback:
                """ Plot the PID feedback in separate plot"""
                ax2 = fig.add_subplot(122)
                ax2.plot([0, len(PIDactionsCopy[0][:])], [0, 0], "k:")
                ax2.plot(PIDactionsCopy[0][:], label="P Action")
                ax2.plot(PIDactionsCopy[1][:], label="I Action")
                ax2.plot(PIDactionsCopy[2][:], label="D Action")
                ax2.title.set_text('PID actions over Time')

                plt.xlabel('Time [0.01s]')
                plt.ylabel('Feedback action [1024 = 5V = max]')
                plt.legend()
                
            figtitle = (str(title))
            plt.figtext(0.5, 0.01, ("overshoot=" + str(round(overshoot, 2)) + " [mm/s]" +
                "   risetime=" + str(risetime) + " [s]" +
                "   settletime=" + str(settletime) + " [s]"),
                ha="center",
                fontsize=12,
                bbox={"facecolor": "salmon", "alpha": 0.3, "pad": 5})
            fig.suptitle(figtitle,
                va='top',
                ha="center",
                fontsize=12,
                bbox={"facecolor": "aquamarine", "alpha": 0.3, "pad": 5})
            plt.subplots_adjust(top=0.5)
            fig.tight_layout(pad=3)  # otherwise the right y-label is slightly clipped
            plt.show()

            if save:
                # Save the Data as .txt files and the figure as .png
                title = title.replace(" ", "")
                filename_png = title + ".png"
                fig.savefig(filename_png)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass
