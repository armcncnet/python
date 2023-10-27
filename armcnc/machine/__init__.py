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
        self.axis_tmp = ""
        self.is_alive = False
        self.info = None
        self.machine_path = ""
        self.workspace = "/opt/armcnc"
        self.task_state = False

    def get_num_axis(self, axis):
        self.axis_tmp = ''.join(self.axis)
        num = self.axis_tmp.find(axis.upper())
        return num

    def get_num(self, axis):
        self.axis_tmp = "XYZABCUVW"
        num = self.axis_tmp.find(axis.upper())
        return num
