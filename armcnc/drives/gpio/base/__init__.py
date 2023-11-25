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
        self.hal = None
        self.gpio = GPIO

    def setup(self):
        if self.father.coordinates != "" and self.father.machine.machine_path != "":
            self.gpio.setmode(GPIO.BCM)
            self.hal = hal.component("armcncio")
            self.hal.newpin("gpio.estop", hal.HAL_BIT, hal.HAL_IN)
            self.hal.ready()

    def loop(self):
        if self.hal and self.father.coordinates != "" and self.father.machine.machine_path != "":
            time.sleep(0.01)

