"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import linuxcnc

class LinuxCNC:

    def __init__(self, framework):
        self.framework = framework
        self.linuxcnc = linuxcnc

