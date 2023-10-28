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
        self.status = False
        self.task = False
        self.joy_x = []
        self.joy_y = []
        self.joy_z = []
        self.joy_a = []
        self.write = "01 03 04 7D 00 07 95 20".encode("utf-8")
        self.read = ""
        self.read_count = 0
        self.joy_speed = {}
        self.joy_count_time = 0
        self.info_count_time = 0
        self.joy = 0
        self.joy_axis = False
        self.joy_rate = 0
        self.last_joy_value = 0
        self.use_joy = False
        self.axis_num = 3
        self.first_run = True
        self.last_joy_speed = 0
        self.joy_dir = True
        self.last_jpy_dir = None
        self.last_joy_dir_count = 0

    def init_serial(self):
        if os.path.exists("/dev/ttyUSB0"):
            self.serial = serial.Serial()
            self.serial.port = "/dev/ttyUSB0"
            self.serial.baudrate = 19200
            try:
                self.serial.open()
                self.task = threading.Thread(name="handwheel_task", target=self.task_work)
                self.task.daemon = True
                self.task.start()
                self.status = True
            except serial.SerialException as e:
                self.status = False

    def task_work(self):
        while True:
            if self.status:
                if len(self.joy_speed) == 0:
                    if len(self.package.framework.machine.axis) > 0:
                        config = configparser.ConfigParser()
                        config.read(self.package.framework.machine.workspace + "/configs/" + self.package.framework.machine.machine_path + "/machine.user")
                        items = config.items("HANDWHEEL")
                        for key, val in items:
                            key = "EXTINFO_" + key.upper()
                            self.joy_speed[key] = float(val.strip())
                        print("joy_speed-->", self.joy_speed)
                    continue
                if self.joy_count_time > 1:
                    print("joy_count_time-->", self.joy_count_time)
                    self.do_joy()
                    self.joy_count_time = 0
                if self.info_count_time > 60:
                    print("info_count_time-->", self.info_count_time)
                    self.set_axis_num()
                    self.info_count_time = 0
                self.info_count_time = self.info_count_time + 1
                self.read = ""
                self.read_count = self.serial.inWaiting()
                if self.read_count != 0:
                    read_tmp = self.serial.read(self.read_count)
                    print("read_tmp-->", read_tmp)
                    self.read = str(binascii.b2a_hex(read_tmp))[6:34]
                    print("read-->", self.read)
                self.serial.flushInput()
                self.joy_count_time = self.joy_count_time + 1
                self.serial.write(self.write)
                if self.read_count == 0 or self.read == "":
                    continue
                self.joy = self.read[0:4]
                self.joy = self.str2hex(self.joy)
                print("joy-->", self.joy)
                self.joy_axis = self.read[8:12]
                self.joy_axis = self.str2hex(self.joy_axis)
                print("joy_axis-->", self.joy_axis)
                self.joy_rate = self.read[12:16]
                self.joy_rate = self.str2hex(self.joy_rate)
                print("joy_rate-->", self.joy_rate)
                if self.first_run:
                    self.last_joy_value = self.joy
                    self.first_run = False
                print("last_joy_value-->", self.last_joy_value)
                joy_rate_tmp = 10
                if self.joy_rate == 171:
                    joy_rate_tmp = 1
                elif self.joy_rate == 86:
                    joy_rate_tmp = 10
                elif self.joy_rate == 0:
                    joy_rate_tmp = 100
                if self.last_joy_value != self.joy:
                    step_tmp = 0
                    step_tmp = self.joy - self.last_joy_value
                    self.last_joy_value = self.joy
                    if step_tmp > 30000:
                        step_tmp = 0 - (65536 - step_tmp)
                    if step_tmp < -30000:
                        step_tmp = 65536 + step_tmp
                    if step_tmp > 100 or step_tmp < -100:
                        continue
                    if self.joy_rate == 255:
                        self.use_joy = True
                        if self.joy_axis == 101:
                            axis = 0
                        if self.joy_axis == 152:
                            axis = 1
                        if self.joy_axis == 204:
                            axis = 2
                        if self.joy_axis == 255:
                            axis = self.axis_num
                        jog_speed_tmp = self.get_joy_speed(axis)
                        if step_tmp < 0:
                            joy_continuous_speed = 0 - jog_speed_tmp
                        elif step_tmp > 0:
                            joy_continuous_speed = jog_speed_tmp
                        if joy_continuous_speed < 0:
                            self.joy_dir = False
                        else:
                            self.joy_dir = True
                        if self.last_jpy_dir != self.joy_dir:
                            self.last_joy_dir_count = self.last_joy_dir_count + 1
                        if self.last_joy_dir_count > 1:
                            self.last_jpy_dir = self.joy_dir
                            self.last_joy_dir_count = 0
                            self.last_joy_speed = joy_continuous_speed
                        self.package.framework.armcnc.command.jog_continuous(axis, self.last_joy_speed, "")
                    else:
                        joy_length_tmp = joy_rate_tmp * step_tmp
                        if self.joy_axis == 101:
                            self.joy_x.append(joy_length_tmp)
                        if self.joy_axis == 152:
                            self.joy_y.append(joy_length_tmp)
                        if self.joy_axis == 204:
                            self.joy_z.append(joy_length_tmp)
                        if self.joy_axis == 255:
                            self.joy_a.append(joy_length_tmp)
                elif self.use_joy:
                    if self.joy_axis == 101:
                        self.package.framework.armcnc.command.jog_stop(0, "")
                    if self.joy_axis == 152:
                        self.package.framework.armcnc.command.jog_stop(1, "")
                    if self.joy_axis == 204:
                        self.package.framework.armcnc.command.jog_stop(2, "")
                    if self.joy_axis == 255:
                        self.package.framework.armcnc.command.jog_stop(self.axis_num, "")
                    self.last_joy_speed = 0
                    self.last_jpy_dir = None
                    self.use_joy = False
            self.package.framework.utils.set_sleep(0.1)

    def do_joy(self):
        jog_length = 0
        if len(self.joy_x) > 0:
            jog_length = self.count_joy_value(self.joy_x)
            print("do_joy-->", jog_length)
            self.joy_x = []
            self.joy_increment(jog_length, 0)
        if len(self.joy_y) > 0:
            jog_length = self.count_joy_value(self.joy_y)
            self.joy_y = []
            self.joy_increment(jog_length, 1)
        if len(self.joy_z) > 0:
            jog_length = self.count_joy_value(self.joy_z)
            self.joy_z = []
            self.joy_increment(jog_length, 2)
        if len(self.joy_a) > 0:
            jog_length = self.count_joy_value(self.joy_a)
            self.joy_a = []
            self.joy_increment(jog_length, self.axis_num)
        return jog_length

    def count_joy_value(self, jog):
        jog_length = 0
        if self.status:
            for i in jog:
                jog_length = jog_length + i
        return float(jog_length) / 100

    def get_joy_speed(self, axis):
        joy_speed = 1000
        if axis == 0:
            joy_speed = self.joy_speed['EXTINFO_JOY_X_VELOCITY']
        elif axis == 1:
            joy_speed = self.joy_speed['EXTINFO_JOY_Y_VELOCITY']
        elif axis == 2:
            joy_speed = self.joy_speed['EXTINFO_JOY_Z_VELOCITY']
        else:
            joy_speed = self.joy_speed['EXTINFO_JOY_A_VELOCITY']
        return joy_speed / 60

    def set_axis_num(self):
        axis = self.package.framework.machine.axis
        print("set_axis_num-->", axis)
        self.axis_num = 3
        # if len(axis) < 4:
        #     print("set_axis_num return---->", len(axis))
        #     return
        # axis_tmp = axis[3]
        # axis_tmp = axis_tmp.upper()
        # if self.package.framework.armcnc.command.is_all_homed() and axis_tmp != "A":
        #     self.axis_num = 4

    def str2hex(self, joy):
        data = 0
        if self.status:
            su = joy.upper()
            for c in su:
                tmp = ord(c)
                if tmp <= ord("9"):
                    data = data << 4
                    data += tmp - ord("0")
                elif ord("A") <= tmp <= ord("F"):
                    data = data << 4
                    data += tmp - ord("A") + 10
        return data

    def joy_increment(self, length, axis):
        speed = self.get_joy_speed(axis)
        self.package.framework.armcnc.command.jog_increment(axis, speed, length, "")
