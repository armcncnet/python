"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import os
import serial
import binascii
import threading
import configparser

class HandWheel:

    def __init__(self, package):
        self.package = package
        self.serial = None
        self.serial_status = False
        self.serial_task = None
        self.write_char = "01 03 04 7D 00 07 95 20"
        self.jog = 0
        self.jog_axis = False
        self.jog_rate = 0
        self.jog_speed = {}
        self.last_jog_speed = 0
        self.jog_count_time = 0
        self.jog_x = []
        self.jog_y = []
        self.jog_z = []
        self.jog_a = []
        self.axis_num = 3
        self.info_count_time = 0
        self.first_run = True
        self.last_Jog_value = 0
        self.use_jog = False
        self.jog_dir = True
        self.last_jog_dir = None
        self.last_jog_dir_count = 0

    def init_serial(self):
        if os.path.exists("/dev/ttyUSB0"):
            self.serial = serial.Serial()
            self.serial.port = "/dev/ttyUSB0"
            self.serial.baudrate = 19200
            self.serial.bytesize = 8
            self.serial.stopbits = serial.STOPBITS_ONE
            self.serial.parity = serial.PARITY_NONE
            try:
                self.serial.open()
                self.serial_task = threading.Thread(name="package_handwheel_task", target=self.task)
                self.serial_task.daemon = True
                self.serial_task.start()
                self.serial_status = True
            except Exception as e:
                self.serial_status = False

    def task(self):
        self.jog_speed = {}
        config = configparser.ConfigParser()
        config.read(self.package.framework.machine.workspace + "/configs/" + self.package.framework.machine.machine_path + "/machine.user")
        config_items = config.items("HANDWHEEL")
        for key, val in config_items:
            key = "EXTINFO_" + key
            self.jog_speed[key] = float(val.strip())
        self.write_char = self.write_char.encode("utf-8")
        while True:
            if self.serial_status:
                if self.jog_count_time > 1:
                    self.do_jog()
                    self.jog_count_time = 0
                if self.info_count_time > 60:
                    self.set_axis_num()
                    self.info_count_time = 0
                self.info_count_time = self.info_count_time + 1
                recv_str = ""
                count = self.serial.inWaiting()
                if count != 0:
                    recv = self.serial.read(count)
                    recv_str = str(binascii.b2a_hex(recv))[6:34]
                self.serial.flushInput()
                self.jog_count_time = self.jog_count_time + 1
                self.serial.write(self.write_char)
                if count == 0:
                    continue
                self.jog = recv_str[0:4]
                self.jog = self.str2hex(self.jog)
                self.jog_axis = recv_str[8:12]
                self.jog_axis = self.str2hex(self.jog_axis)
                self.jog_rate = recv_str[12:16]
                self.jog_rate = self.str2hex(self.jog_rate)
                if self.first_run:
                    self.last_Jog_value = self.jog
                    self.first_run = False
                jog_rate = 10
                if self.jog_rate == 171:
                    jog_rate = 1
                if self.jog_rate == 86:
                    jog_rate = 10
                if self.jog_rate == 0:
                    jog_rate = 100
                if self.last_Jog_value != self.jog:
                    step = 0
                    step = self.jog - self.last_Jog_value
                    self.last_Jog_value = self.jog
                    if step > 30000:
                        step = 0 - (65536 - step)
                    if step < -30000:
                        step = 65536 + step
                    if step > 100 or step < -100:
                        continue
                    if self.jog_rate == 255:
                        self.use_jog = True
                        axis = 0
                        if self.jog_axis == 101:
                            axis = 0
                        if self.jog_axis == 152:
                            axis = 1
                        if self.jog_axis == 204:
                            axis = 2
                        if self.jog_axis == 255:
                            axis = self.axis_num
                        jog_speed = self.get_jog_speed(axis)
                        jog_continuous_speed = 0
                        if step < 0:
                            jog_continuous_speed = 0 - jog_speed
                        elif step > 0:
                            jog_continuous_speed = jog_speed
                        if jog_continuous_speed < 0:
                            self.jog_dir = False
                        else:
                            self.jog_dir = True
                        if self.last_jog_dir != self.jog_dir:
                            self.last_jog_dir_count = self.last_jog_dir_count + 1
                        if self.last_jog_dir_count > 1:
                            self.last_jog_dir = self.jog_dir
                            self.last_jog_dir_count = 0
                            self.last_jog_speed = jog_continuous_speed
                        self.package.framework.armcnc.command.jog_continuous(axis, self.last_jog_speed, "")
                    else:
                        jog_length = jog_rate * step
                        if self.jog_axis == 101:
                            self.jog_x.append(jog_length)
                        if self.jog_axis == 152:
                            self.jog_y.append(jog_length)
                        if self.jog_axis == 204:
                            self.jog_z.append(jog_length)
                        if self.jog_axis == 255:
                            self.jog_a.append(jog_length)
                elif self.use_jog:
                    if self.jog_axis == 101:
                        self.package.framework.armcnc.command.jog_stop(0, "")
                    if self.jog_axis == 152:
                        self.package.framework.armcnc.command.jog_stop(1, "")
                    if self.jog_axis == 204:
                        self.package.framework.armcnc.command.jog_stop(2, "")
                    if self.jog_axis == 255:
                        self.package.framework.armcnc.command.jog_stop(self.axis_num, "")
                    self.last_jog_speed = 0
                    self.last_jog_dir = None
                    self.use_jog = False
                self.package.framework.utils.set_sleep(0.1)

    def set_axis_num(self):
        axis = self.package.framework.machine.axis
        self.axis_num = 3
        if len(axis) < 4:
            return
        axis_str = axis[3]
        if axis_str != "A":
            self.axis_num = 4

    def do_jog(self):
        jog_length = 0
        if len(self.jog_x) > 0:
            jog_length = self.jog_count_value(self.jog_x)
            self.jog_x = []
            self.send_increment(jog_length, 0)
        if len(self.jog_y) > 0:
            jog_length = self.jog_count_value(self.jog_y)
            self.jog_y = []
            self.send_increment(jog_length, 1)
        if len(self.jog_z) > 0:
            jog_length = self.jog_count_value(self.jog_z)
            self.jog_z = []
            self.send_increment(jog_length, 2)
        if len(self.jog_a) > 0:
            jog_length = self.jog_count_value(self.jog_a)
            self.jog_a = []
            self.send_increment(jog_length, self.axis_num)

    def jog_count_value(self, jog):
        jog_length = 0
        for i in jog:
            jog_length = jog_length + i
        return float(jog_length) / 100

    def get_jog_speed(self, axis):
        speed = 1000
        if axis == 0:
            speed = self.jog_speed["EXTINFO_JOY_X_VELOCITY"]
        if axis == 1:
            speed = self.jog_speed["EXTINFO_JOY_Y_VELOCITY"]
        if axis == 2:
            speed = self.jog_speed["EXTINFO_JOY_Y_VELOCITY"]
        if axis == 3:
            speed = self.jog_speed["EXTINFO_JOY_A_VELOCITY"]
        return speed / 60

    def send_increment(self, length, axis):
        speed = self.get_jog_speed(axis)
        print("--->", speed, axis)
        self.package.framework.armcnc.command.jog_increment(axis, speed, length, "")

    def str2hex(self, jog):
        data = 0
        jog = jog.upper()
        for c in jog:
            tmp = ord(c)
            if tmp <= ord("9"):
                data = data << 4
                data += tmp - ord("0")
            elif ord("A") <= tmp <= ord("F"):
                data = data << 4
                data += tmp - ord("A") + 10
        return data
