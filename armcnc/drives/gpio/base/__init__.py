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
            self.hal = hal.component("armcncio")
            mode = self.gpio.getmode()
            if mode != "BCM":
                self.gpio.setmode(self.gpio.BCM)
            pins = self.father.machine.get_user_config_array("IO")
            for key, val in pins:
                pin = val.strip().split()
                if len(pin) == 3:
                    if pin[2] == "IN":
                        if self.gpio.gpio_function(int(pin[1])) != "IN":
                            self.gpio.setup(int(pin[1]), self.gpio.IN)
                    if pin[2] == "OUT":
                        if self.gpio.gpio_function(int(pin[1])) != "OUT":
                            self.gpio.setup(int(pin[1]), self.gpio.OUT)
                    self.hal.newpin(pin[0], hal.HAL_BIT, hal.HAL_IN)
            self.hal.ready()

    def loop(self):
        if self.hal and self.father.coordinates != "" and self.father.machine.machine_path != "":
            pins = self.father.machine.get_user_config_array("IO")
            for key, val in pins:
                pin = val.strip().split()
                if len(pin) == 3:
                    if pin[2] == "IN" and self.hal[pin[0]]:
                        pin_status = self.gpio.input(int(pin[1]))
                        self.hal[pin[0]] = pin_status
        time.sleep(0.01)

