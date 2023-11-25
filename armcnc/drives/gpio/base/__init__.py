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
        self.estop = None

    def setup(self):
        if self.father.coordinates != "" and self.father.machine.machine_path != "":
            self.hal = hal.component("armcncio")
            mode = self.gpio.getmode()
            if mode != "BCM":
                self.gpio.setmode(self.gpio.BCM)
            estop = self.father.machine.get_user_config_value("IO", "ESTOP_PIN")
            if estop != "":
                self.estop = estop.split()
                if self.estop[2] == "IN":
                    if self.gpio.gpio_function(int(self.estop[1])) != "IN":
                        self.gpio.setup(int(self.estop[1]), self.gpio.IN)
                if self.estop[2] == "OUT":
                    if self.gpio.gpio_function(int(self.estop[1])) != "OUT":
                        self.gpio.setup(int(self.estop[1]), self.gpio.OUT)
                self.hal.newpin(self.estop[0], hal.HAL_BIT, hal.HAL_IN)
            self.hal.ready()

    def loop(self):
        if self.hal and self.father.coordinates != "" and self.father.machine.machine_path != "":
            if self.estop:
                if self.hal[self.estop[0]]:
                    estop_status = self.gpio.input(int(self.estop[1]))
                    self.hal[self.estop[0]] = estop_status
        time.sleep(0.01)

