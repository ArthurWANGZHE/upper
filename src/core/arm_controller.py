# 实现点动、寸动以及急停
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer

from src.core.Delta_robot import DeltaRobotKinematics
from src.communication.communication import Communication



# from utils import ws
# model_filename=""
class ArmController(QObject):
    x_changed = pyqtSignal(str)
    y_changed = pyqtSignal(str)
    z_changed = pyqtSignal(str)
    t1_changed = pyqtSignal(str)
    t2_changed = pyqtSignal(str)
    t3_changed = pyqtSignal(str)

    def __init__(self):
        super(ArmController, self).__init__()
        self.robot = DeltaRobotKinematics(133,
                                          60,
                                          251,
                                          300)
        self.communication = Communication()
        self.timer=QTimer()

        self.timer.timeout.connect(self.on_timeout)

        self.start_timer()

    def start_timer(self):
        # 设置定时器为单次触发，并设置间隔为1000毫秒（1秒）
        self.timer.setSingleShot(True)
        self.timer.start(10)

    def on_timeout(self):
        return


    # 沿着x轴移动
    def move_arm_x(self, distance):
        self.communication.send_data("FF 40 FE")
        x1, y1, z1 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        self.robot.xyz[0] = self.robot.xyz[0] + distance
        x2, y2, z2 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        points, velocity, acceleration, jerk = self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2])
        self.robot.t = t_new
        self.up_xyz()
        self.up_t()
        return

    # 沿着y轴移动
    def move_arm_y(self, distance):
        self.communication.send_data("FF 40 FE")
        x1, y1, z1 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        self.robot.xyz[1] = self.robot.xyz[1] + distance
        x2, y2, z2 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        points, velocity, acceleration, jerk = self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2])
        self.robot.t = t_new
        self.up_xyz()
        self.up_t()
        return

    # 沿着z轴移动
    def move_arm_z(self, distance):
        self.communication.send_data("FF 40 FE")
        x1, y1, z1 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        self.robot.xyz[2] = self.robot.xyz[2] + distance
        x2, y2, z2 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        points, velocity, acceleration, jerk = self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2])
        self.robot.t = t_new
        self.up_xyz()
        self.up_t()
        return

    # 指定点到点
    def move_arm_2p(self, x_n, y_n, z_n):
        self.communication.send_data("FF 40 FE")
        x1, y1, z1 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        x2, y2, z2 = x_n, y_n, z_n
        self.robot.xyz = [x_n, y_n, z_n]
        points, velocity, acceleration, jerk = self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2])
        self.robot.t = t_new
        self.up_xyz()
        self.up_t()
        return

    def run_curve(self, a):
        if a == "门型曲线":
            self.gate_curve()
        elif a == "花朵":
            self.flower()
        elif a == 2:
            self.lame()
        elif a == 3:
            self.ph()
        return

    def gate_curve(self):
        # 归零
        # ff0x02fe
        self.point2point(0, -50, -300)
        self.communication.send_data("FF 40 FE")
        # 门型曲线
        points, velocity, acceleration, jerk = self.robot.gate_curve()
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)


        self.robot.xyz=[0, 50, -380]
        t_new = self.robot.forward_kinematics(self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2])
        self.robot.t = t_new
        self.up_xyz()
        self.up_t()
        return

    def flower(self):
        self.point2point(35.5,0,-380)
        # 花朵
        points, velocity, acceleration, jerk = self.robot.flower()
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        self.communication.send_data("FF 40 FE")


        self.robot.xyz=[37.5, 0, -380]
        t_new = self.robot.forward_kinematics(self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2])
        self.robot.t = t_new
        self.up_xyz()
        self.up_t()
        return


    def lame(self):
        pass

    def ph(self):
        pass

    # 急停
    def stop(self):
        # 构建急停命令
        command = "FF 10 FE"
        self.communication.send_data(command)
        return

    def back(self):

        self.communication.send_data("FF 20 FE")
        self.robot.xyz=[0.0, 0.0, -273.92]
        self.robot.t = [0, 0, 0]



        response = self.communication.receive_data()
        while response == "":
            self.timer.start()
            response = self.communication.receive_data()

        if response == "FF 80 FE":
            self.move_arm_z(-10)

        return

    def point2point(self, x2, y2, z2):
        self.communication.send_data("FF 40 FE")
        x1, y1, z1 = self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2]
        self.robot.xyz = [x1, y1, z1]
        points, velocity, acceleration, jerk = self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0], self.robot.xyz[1], self.robot.xyz[2])
        self.robot.t = t_new
        self.up_xyz()
        self.up_t()
        return

    def classify(self):
        pass

    def pick(self):
        pass

    def move_a_up(self):
        while True:
            self.communication.send_data("FF 30 0100 0000 0000 00 00 FE")
            self.start_timer()
            self.start_timer()
        return

    def move_a_down(self):
        while True:
            self.communication.send_data("FF 30 0101 0000 0000 00 00 FE")
            self.start_timer()
            self.start_timer()
        return

    def move_b_up(self):
        while True:
            self.communication.send_data("FF 30 0000 0100 0000 00 00 FE")
            self.start_timer()
            self.start_timer()
        return

    def move_b_down(self):
        while True:

            self.communication.send_data("FF 30 0000 0101 0000 00 00 FE")
            self.start_timer()
            self.start_timer()





    def move_c_up(self):
        while True:

            self.communication.send_data("FF 30 0000 0000 0100 00 00 FE")
            self.start_timer()
            self.start_timer()
        return

    def move_c_down(self):
        while True:
            self.communication.send_data("FF 30 0000 0000 0101 00 00 FE")
            self.start_timer()
            self.start_timer()



    def x_up(self):
        self.move_arm_x(10)
        return

    def x_down(self):
        self.move_arm_x(-10)
        return

    def y_up(self):

        self.move_arm_y(10)
        return

    def y_down(self):

        self.move_arm_y(-10)
        return

    def z_up(self):
        self.move_arm_z(10)
        return

    def z_down(self):

        self.move_arm_z(-10)
        return

    def a_up(self):

        self.move_a_up()
        return

    def a_down(self):

        self.move_a_down()
        return

    def b_up(self):

        self.move_b_up()
        return

    def b_down(self):

        self.move_b_down()
        return

    def c_up(self):

        self.move_c_up()
        return

    def c_down(self):
        while True:
            self.move_c_down()
        return

    def up_t1(self):
        self.t1_changed.emit(str(self.robot.t[0]))
        return

    def up_t2(self):
        self.t2_changed.emit(str(self.robot.t[1]))
        return

    def up_t3(self):
        self.t3_changed.emit(str(self.robot.t[2]))
        return

    def ud_x(self):
        self.x_changed.emit(str(self.robot.xyz[0]))
        return

    def ud_y(self):
        self.y_changed.emit(str(self.robot.xyz[1]))

    def ud_z(self):
        self.z_changed.emit(str(self.robot.xyz[2]))

    def up_xyz(self):
        self.ud_x()
        self.ud_y()
        self.ud_z()

    def up_t(self):
        self.up_t1()
        self.up_t2()
        self.up_t3()
