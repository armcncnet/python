"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

from .handwheel import HandWheel

class Package:

    def __init__(self, framework):
        self.framework = framework
        self.handwheel = HandWheel(self)

