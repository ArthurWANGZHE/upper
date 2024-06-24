from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from arm_controller import ArmController
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.controller = ArmController()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)

        self.move_x_1 = QPushButton(MainWindow)
        self.move_x_1.setGeometry(350, 250, 30, 30)
        self.move_x_1.setObjectName("move_x_1")

        self.move_x_2 = QPushButton(MainWindow)
        self.move_x_2.setGeometry(400, 250, 30, 30)
        self.move_x_2.setObjectName("move_x_2")

        self.move_y_1 = QPushButton(MainWindow)
        self.move_y_1.setGeometry(375, 275, 30, 30)
        self.move_y_1.setObjectName("move_y_1")

        self.move_y_2 = QPushButton(MainWindow)
        self.move_y_2.setGeometry(375, 225, 30, 30)
        self.move_y_2.setObjectName("move_y_2")

        self.move_z_1 = QPushButton(MainWindow)
        self.move_z_1.setGeometry(300, 275, 30, 30)
        self.move_z_1.setObjectName("move_z_button")

        self.move_z_2 = QPushButton(MainWindow)
        self.move_z_2.setGeometry(300, 225, 30, 30)
        self.move_z_2.setObjectName("move_z_button")

        self.stop_button = QPushButton(MainWindow)
        self.stop_button.setGeometry(50, 200, 30, 30)
        self.stop_button.setObjectName("stop_button")

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.move_x_1.setText(_translate("MainWindow", "X+"))
        self.move_x_2.setText(_translate("MainWindow", "X-"))
        self.move_y_1.setText(_translate("MainWindow", "Y+"))
        self.move_y_2.setText(_translate("MainWindow", "Y-"))
        self.move_z_1.setText(_translate("MainWindow", "Z+"))
        self.move_z_2.setText(_translate("MainWindow", "Z+"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))

        self.move_x_1.clicked.connect(lambda: self.controller.move_arm_x(1))
        self.move_x_2.clicked.connect(lambda: self.controller.move_arm_x(-1))
        self.move_y_1.clicked.connect(lambda: self.controller.move_arm_y(1))
        self.move_y_2.clicked.connect(lambda: self.controller.move_arm_y(-1))
        self.move_z_1.clicked.connect(lambda: self.controller.move_arm_z(1))
        self.move_z_2.clicked.connect(lambda: self.controller.move_arm_z(-1))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.controller=ArmController()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())