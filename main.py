import sys
from PyQt5.QtWidgets import QApplication
from Ui import MainWindow
from communication import Communication
from arm_controller import ArmController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    arm_controller = ArmController()

    window = MainWindow()
    window.move_x_button.clicked.connect(lambda: arm_controller.move_arm_x(1))  # Move 1 unit along x axis
    window.move_y_button.clicked.connect(lambda: arm_controller.move_arm_y(1))  # Move 1 unit along y axis
    window.move_z_button.clicked.connect(lambda: arm_controller.move_arm_z(1))  # Move 1 unit along z axis
    window.stop_button.clicked.connect(arm_controller.stop)

    window.show()

    sys.exit(app.exec_())