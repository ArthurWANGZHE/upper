from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from UI import Ui_Widget
from arm_controller import ArmController
from camera import Camera
import sys
from camera import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.camera_thread = Camera()
        self.camera_thread.set_cam_number(0)
        # 连接Camera的sendPicture信号与receive函数进行展示
        self.camera_thread.sendPicture[QImage].connect(self.receive)
        self.camera_thread.open_camera()

    def receive(self, img):
        img_height = self.ui.cameraview.height()
        img_width = self.ui.cameraview.width()
        new_img = img.scaled(QSize(img_width, img_height))
        self.ui.cameraview.setPixmap(QPixmap.fromImage(new_img))


if __name__ == "__main__":
    while True:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())