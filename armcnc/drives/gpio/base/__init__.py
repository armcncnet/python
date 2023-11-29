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
        self.x_home = None

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
                    self.hal.newpin(self.estop[0], hal.HAL_BIT, hal.HAL_IN)
                if self.estop[2] == "OUT":
                    if self.gpio.gpio_function(int(self.estop[1])) != "OUT":
                        self.gpio.setup(int(self.estop[1]), self.gpio.OUT)
                    self.hal.newpin(self.estop[0], hal.HAL_BIT, hal.HAL_OUT)
            x_home = self.father.machine.get_user_config_value("IO", "X_HOME_PIN")
            if x_home != "":
                self.x_home = x_home.split()
                if self.x_home[2] == "IN":
                    if self.gpio.gpio_function(int(self.x_home[1])) != "IN":
                        self.gpio.setup(int(self.x_home[1]), self.gpio.IN)
                    self.hal.newpin(self.x_home[0], hal.HAL_BIT, hal.HAL_IN)
                if self.x_home[2] == "OUT":
                    if self.gpio.gpio_function(int(self.x_home[1])) != "OUT":
                        self.gpio.setup(int(self.x_home[1]), self.gpio.OUT)
                    self.hal.newpin(self.x_home[0], hal.HAL_BIT, hal.HAL_OUT)
            self.hal.ready()

    def loop(self):
        if self.hal and self.father.coordinates != "" and self.father.machine.machine_path != "":
            if self.estop:
                estop_status = self.gpio.input(int(self.estop[1]))
                self.hal[self.estop[0]] = estop_status
            if self.x_home:
                x_home_status = self.gpio.input(int(self.x_home[1]))
                self.hal[self.x_home[0]] = x_home_status
        time.sleep(0.005)
