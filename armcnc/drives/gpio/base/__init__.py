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
        self.y_home = None
        self.z_home = None
        self.a_home = None
        self.b_home = None
        self.c_home = None

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
            y_home = self.father.machine.get_user_config_value("IO", "Y_HOME_PIN")
            if y_home != "":
                self.y_home = y_home.split()
                if self.y_home[2] == "IN":
                    if self.gpio.gpio_function(int(self.y_home[1])) != "IN":
                        self.gpio.setup(int(self.y_home[1]), self.gpio.IN)
                    self.hal.newpin(self.y_home[0], hal.HAL_BIT, hal.HAL_IN)
                if self.y_home[2] == "OUT":
                    if self.gpio.gpio_function(int(self.y_home[1])) != "OUT":
                        self.gpio.setup(int(self.y_home[1]), self.gpio.OUT)
                    self.hal.newpin(self.y_home[0], hal.HAL_BIT, hal.HAL_OUT)
            z_home = self.father.machine.get_user_config_value("IO", "Z_HOME_PIN")
            if z_home != "":
                self.z_home = z_home.split()
                if self.z_home[2] == "IN":
                    if self.gpio.gpio_function(int(self.z_home[1])) != "IN":
                        self.gpio.setup(int(self.z_home[1]), self.gpio.IN)
                    self.hal.newpin(self.z_home[0], hal.HAL_BIT, hal.HAL_IN)
                if self.z_home[2] == "OUT":
                    if self.gpio.gpio_function(int(self.z_home[1])) != "OUT":
                        self.gpio.setup(int(self.z_home[1]), self.gpio.OUT)
                    self.hal.newpin(self.z_home[0], hal.HAL_BIT, hal.HAL_OUT)
            a_home = self.father.machine.get_user_config_value("IO", "A_HOME_PIN")
            if a_home != "":
                self.a_home = a_home.split()
                if self.a_home[2] == "IN":
                    if self.gpio.gpio_function(int(self.a_home[1])) != "IN":
                        self.gpio.setup(int(self.a_home[1]), self.gpio.IN)
                    self.hal.newpin(self.a_home[0], hal.HAL_BIT, hal.HAL_IN)
                if self.a_home[2] == "OUT":
                    if self.gpio.gpio_function(int(self.a_home[1])) != "OUT":
                        self.gpio.setup(int(self.a_home[1]), self.gpio.OUT)
                    self.hal.newpin(self.a_home[0], hal.HAL_BIT, hal.HAL_OUT)
            b_home = self.father.machine.get_user_config_value("IO", "B_HOME_PIN")
            if b_home != "":
                self.b_home = b_home.split()
                if self.b_home[2] == "IN":
                    if self.gpio.gpio_function(int(self.b_home[1])) != "IN":
                        self.gpio.setup(int(self.b_home[1]), self.gpio.IN)
                    self.hal.newpin(self.b_home[0], hal.HAL_BIT, hal.HAL_IN)
                if self.b_home[2] == "OUT":
                    if self.gpio.gpio_function(int(self.b_home[1])) != "OUT":
                        self.gpio.setup(int(self.b_home[1]), self.gpio.OUT)
                    self.hal.newpin(self.b_home[0], hal.HAL_BIT, hal.HAL_OUT)
            c_home = self.father.machine.get_user_config_value("IO", "C_HOME_PIN")
            if c_home != "":
                self.c_home = c_home.split()
                if self.c_home[2] == "IN":
                    if self.gpio.gpio_function(int(self.c_home[1])) != "IN":
                        self.gpio.setup(int(self.c_home[1]), self.gpio.IN)
                    self.hal.newpin(self.c_home[0], hal.HAL_BIT, hal.HAL_IN)
                if self.c_home[2] == "OUT":
                    if self.gpio.gpio_function(int(self.c_home[1])) != "OUT":
                        self.gpio.setup(int(self.c_home[1]), self.gpio.OUT)
                    self.hal.newpin(self.c_home[0], hal.HAL_BIT, hal.HAL_OUT)
            self.hal.ready()

    def loop(self):
        if self.hal and self.father.coordinates != "" and self.father.machine.machine_path != "":
            if self.estop:
                estop_status = self.gpio.input(int(self.estop[1]))
                self.hal[self.estop[0]] = estop_status
            if self.x_home:
                x_home_status = self.gpio.input(int(self.x_home[1]))
                if len(self.x_home) == 4 and self.x_home[3] == "NOT":
                    x_home_status = not x_home_status
                self.hal[self.x_home[0]] = x_home_status
            if self.y_home:
                y_home_status = self.gpio.input(int(self.y_home[1]))
                if len(self.y_home) == 4 and self.y_home[3] == "NOT":
                    y_home_status = not y_home_status
                self.hal[self.y_home[0]] = y_home_status
            if self.z_home:
                z_home_status = self.gpio.input(int(self.z_home[1]))
                if len(self.z_home) == 4 and self.z_home[3] == "NOT":
                    z_home_status = not z_home_status
                self.hal[self.z_home[0]] = z_home_status
            if self.a_home:
                a_home_status = self.gpio.input(int(self.a_home[1]))
                if len(self.a_home) == 4 and self.a_home[3] == "NOT":
                    a_home_status = not a_home_status
                self.hal[self.a_home[0]] = a_home_status
            if self.b_home:
                b_home_status = self.gpio.input(int(self.b_home[1]))
                if len(self.b_home) == 4 and self.b_home[3] == "NOT":
                    b_home_status = not b_home_status
                self.hal[self.b_home[0]] = b_home_status
            if self.c_home:
                c_home_status = self.gpio.input(int(self.c_home[1]))
                if len(self.c_home) == 4 and self.c_home[3] == "NOT":
                    c_home_status = not c_home_status
                self.hal[self.c_home[0]] = c_home_status
        time.sleep(0.002)
