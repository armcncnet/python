"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import linuxcnc

class Error:

    def __init__(self):
        self.apis = linuxcnc.command()
