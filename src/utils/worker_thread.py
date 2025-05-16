from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic.properties import QtCore

from src.core.arm_controller import ArmController
from src.communication.communication import Communication

class WorkerThread(QThread):
    armcontroller = ArmController()
    def __init__(self, method_name, *args, **kwargs):
        super().__init__()
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        WorkerThread.armcontroller.x_changed.connect(self.xxx)
        WorkerThread.armcontroller.y_changed.connect(self.yyy)
        WorkerThread.armcontroller.z_changed.connect(self.zzz)
        WorkerThread.armcontroller.t1_changed.connect(self.t11)
        WorkerThread.armcontroller.t2_changed.connect(self.t22)
        WorkerThread.armcontroller.t3_changed.connect(self.t33)
        WorkerThread.armcontroller.communication.sent_data.connect(self.message)
        WorkerThread.armcontroller.communication.recieved_respond.connect(self.respond)

    def run(self):
        # 检查 ArmController 实例中是否包含通信对象和方法
        if hasattr(WorkerThread.armcontroller, self.method_name):
            getattr(WorkerThread.armcontroller, self.method_name)(*self.args, **self.kwargs)
        elif hasattr(WorkerThread.armcontroller.communication, self.method_name):
            # 调用 Communication 的方法
            getattr(WorkerThread.armcontroller.communication, self.method_name)(*self.args, **self.kwargs)
        else:
            print(f"Method {self.method_name} not found in Communication class.")

    def xxx(self, message):
        self.emit(QtCore.SIGNAL("ux"),message)


    def yyy(self, message):
        self.emit(QtCore.SIGNAL("uy"),message)



    def zzz(self, message):
        self.emit(QtCore.SIGNAL("uz"),message)


    def t11(self, message):
        self.emit(QtCore.SIGNAL("t11"),message)


    def t22(self, message):
        self.emit(QtCore.SIGNAL("t22"),message)


    def t33(self, message):
        self.emit(QtCore.SIGNAL("t33"), message)

    def respond(self, message):
        self.emit(QtCore.SIGNAL("respond"), message)


    def message(self, message):
        self.emit(QtCore.SIGNAL("message"), message)