from PyQt5 import QtWidgets
from UI import Ui_MainWindow
from arm_controller import ArmController
from communication import Communication
"""
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        """
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.arm = ArmController()
        self.com = Communication()

        # Connect buttons to their functions
        self.btnOpen_2.clicked.connect(lambda: self.arm.move_arm_x(2))
        self.btnOpen_3.clicked.connect(lambda: self.arm.move_arm_x(-2))
        self.btnOpen_4.clicked.connect(lambda: self.arm.move_arm_y(2))
        self.btnOpen_5.clicked.connect(lambda: self.arm.move_arm_y(-2))
        self.btnOpen_6.clicked.connect(lambda: self.arm.move_arm_z(2))
        self.btnOpen_7.clicked.connect(lambda: self.arm.move_arm_z(-2))
        self.btnOpen.clicked.connect(self.com.open_serial)
        self.btnSend.clicked.connect(lambda: self.com.send_data(self.txt1.text()))
        self.btnOpen_8.clicked.connect(lambda: self.arm.move_arm_x(2))
        self.btnOpen_9.clicked.connect(lambda: self.arm.move_arm_x(-2))
        self.btnOpen_10.clicked.connect(lambda: self.arm.move_arm_y(2))
        self.btnOpen_11.clicked.connect(lambda: self.arm.move_arm_y(-2))
        self.btnOpen_12.clicked.connect(lambda: self.arm.move_arm_z(2))
        self.btnOpen_13.clicked.connect(lambda: self.arm.move_arm_z(-2))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()