"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import os
import serial
import threading

class HandWheel:

    def __init__(self, package):
        self.package = package
        self.serial = None
        self.serial_status = False
        self.serial_task = None

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
                self.serial_status = True
            except Exception as e:
                self.serial_status = False

    def task(self):
        while True:
            if self.serial_status:
                pass


