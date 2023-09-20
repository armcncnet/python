"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import linuxcnc

class Statistics:

    def __init__(self):
        self.api = linuxcnc.stat()
