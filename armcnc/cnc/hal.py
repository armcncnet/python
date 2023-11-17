"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import hal
import linuxcnc

class Hal:

    def __init__(self, father):
        self.father = father
        self.linuxcnc = linuxcnc
        self.hal = hal
