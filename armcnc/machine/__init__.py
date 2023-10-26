"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

class Machine:

    def __init__(self, framework):
        self.framework = framework
        self.user = "armcnc"
        self.axis = []
        self.is_alive = False
        self.info = None
        self.axes_tmp = ""

    def get_num_axis(self, axis):
        self.axes_tmp = ''.join(self.axis)
        num = self.axes_tmp.find(axis.upper())
        return num

    def get_num(self, axis):
        self.axes_tmp = "XYZABCUVW"
        num = self.axes_tmp.find(axis.upper())
        return num
