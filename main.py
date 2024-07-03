from PyQt5 import QtWidgets

from UI import Ui_Widget
from arm_controller import ArmController
from communication import Communication


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.arm = ArmController()
        self.com = Communication()
        self.connect_signal()

        self.ui.pushButton.clicked.connect(lambda:self.com.connect())
        self.ui.pushButton_2.clicked.connect(lambda:self.arm.stop())
        self.ui.pushButton_3.clicked.connect(lambda:self.arm.back())
        self.ui.pushButton_4.clicked.connect(lambda:self.arm.classify())
        self.ui.pushButton_5.clicked.connect(lambda:self.arm.pick())
        self.ui.pushButton_6.clicked.connect(lambda:self.arm.run_carve(self.ui.get_curve()))
        self.ui.pushButton_7.clicked.connect(lambda:self.arm.point2point(self.ui.get_xyz()))
        self.ui.pushButton_8.clicked.connect(lambda:self.arm.x_up())
        self.ui.pushButton_9.clicked.connect(lambda:self.arm.x_down())
        self.ui.pushButton_10.clicked.connect(lambda:self.arm.y_up())
        self.ui.pushButton_11.clicked.connect(lambda:self.arm.y_down())
        self.ui.pushButton_12.clicked.connect(lambda:self.arm.z_up())
        self.ui.pushButton_13.clicked.connect(lambda:self.arm.z_down())
        self.ui.pushButton_14.clicked.connect(lambda:self.arm.a_up())
        self.ui.pushButton_15.clicked.connect(lambda:self.arm.a_down())
        self.ui.pushButton_16.clicked.connect(lambda:self.arm.b_up())
        self.ui.pushButton_17.clicked.connect(lambda:self.arm.b_down())
        self.ui.pushButton_18.clicked.connect(lambda:self.arm.c_up())
        self.ui.pushButton_19.clicked.connect(lambda:self.arm.c_down())


    def connect_signal(self):
        self.arm.x_changed.connect(self.xxx)
        self.arm.y_changed.connect(self.yyy)
        self.arm.z_changed.connect(self.zzz)
        self.arm.t1_changed.connect(self.t11)
        self.arm.t2_changed.connect(self.t22)
        self.arm.t3_changed.connect(self.t33)
        self.com.sent_data.connect(self.message)
        self.com.recieved_respond.connect(self.respond)


    def xxx(self,message):
        self.ui.textBrowser_6.append(message)

    def yyy(self,message):
        self.ui.textBrowser_7.append(message)

    def zzz(self,message):
        self.ui.textBrowser_8.append(message)

    def t11(self,message):
        self.ui.textBrowser_3.append(message)

    def t22(self,message):
        self.ui.textBrowser_4.append(message)

    def t33(self,message):
        self.ui.textBrowser_5.append(message)

    def respond(self,message):
        self.ui.textBrowser.append(message)

    def message(self,message):
        self.ui.textBrowser_2.append(message)






if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()