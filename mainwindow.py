from PyQt5.QtWidgets import QMainWindow
from communication import Communication
from arm_controller import ArmController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.communication = Communication()
        self.arm_controller = ArmController(self.communication)


    def move_arm(self):
        # 调用机械臂控制逻辑
        self.arm_controller.move_arm()
