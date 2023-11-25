"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import hal
import time
import Hobot.GPIO as GPIO

class Base:

    def __init__(self, father):
        self.father = father
        self.hal = hal
        self.gpio = GPIO

    def setup(self):
        if self.father.coordinates != "" and self.father.machine.machine_path != "":
            self.gpio.setmode(GPIO.BCM)

    def loop(self):
        if self.father.coordinates != "" and self.father.machine.machine_path != "":
            time.sleep(0.01)

