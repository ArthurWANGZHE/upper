# 实现点动、寸动以及急停
from PyQt5.QtCore import QObject, pyqtSignal

from Delta_robot import DeltaRobotKinematics
from communication import Communication


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
        """
        self.x_changed = pyqtSignal(str)
        self.y_changed = pyqtSignal(str)
        self.z_changed = pyqtSignal(str)
        self.t1_changed = pyqtSignal(str)
        self.t2_changed = pyqtSignal(str)
        self.t3_changed = pyqtSignal(str)
        """
        # classifier = load(model_filename)

    """
    def cal_ws(self):
        if self.robot.xyz in ws:
            pass
        else:
            return Exception
    """

    # 沿着x轴移动
    def move_arm_x(self, distance):
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

    def run_carve(self, a):
        if a == 0:
            self.gate_curve()
        elif a == 1:
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
        # 门型曲线
        points, velocity, acceleration, jerk = self.robot.gate_curve()
        packages = self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        self.communication.send_data("FF 10 FE")
        self.up_xyz()
        self.up_t()
        return

    def flower(self):
        pass

    def lame(self):
        pass

    def ph(self):
        pass

    # 急停
    def stop(self):
        # 构建急停命令
        command = "FF 11 FE"
        self.communication.send_data(command)
        return

    def back(self):
        command1 = "FF 12 FE"
        command2 = "FF 10 FE"
        self.communication.send_data(command1)
        self.communication.send_data(command2)

        return

    def point2point(self, x2, y2, z2):
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
        self.communication.send_data("FF 30 0100 0000 0000 00 00 FE")
        return

    def move_a_down(self):
        self.communication.send_data("FF 30 0101 0000 0000 00 00 FE")
        return

    def move_b_up(self):
        self.communication.send_data("FF 30 0000 0100 0000 00 00 FE")
        return

    def move_b_down(self):
        self.communication.send_data("FF 30 0000 0101 0000 00 00 FE")
        return

    def move_c_up(self):
        self.communication.send_data("FF 30 0000 0000 0100 00 00 FE")
        return

    def move_c_down(self):
        self.communication.send_data("FF 30 0000 0000 0101 00 00 FE")
        return

    def x_up(self, checked):
        if checked:
            self.move_arm_x(1)
        return

    def x_down(self, checked):
        if checked:
            self.move_arm_x(-1)
        return

    def y_up(self, checked):
        if checked:
            self.move_arm_y(1)
        return

    def y_down(self, checked):
        if checked:
            self.move_arm_y(-1)
        return

    def z_up(self, checked):
        if checked:
            self.move_arm_z(1)
        return

    def z_down(self, checked):
        if checked:
            self.move_arm_z(-1)
        return

    def a_up(self, checked):
        if checked:
            self.move_a_up()
        return

    def a_down(self, checked):
        if checked:
            self.move_a_down()
        return

    def b_up(self, checked):
        if checked:
            self.move_b_up()
        return

    def b_down(self, checked):
        if checked:
            self.move_b_down()
        return

    def c_up(self, checked):
        if checked:
            self.move_c_up()
        return

    def c_down(self, checked):
        if checked:
            self.move_c_down()
        return

    def up_t1(self):
        self.t1_changed.emit(self.robot.t[0])
        return

    def up_t2(self):
        self.t2_changed.emit(self.robot.t[1])
        return

    def up_t3(self):
        self.t3_changed.emit(self.robot.t[2])
        return

    def ud_x(self):
        self.x_changed.emit(self.robot.xyz[0])
        return

    def ud_y(self):
        self.y_changed.emit(self.robot.xyz[1])

    def ud_z(self):
        self.z_changed.emit(self.robot.xyz[2])

    def up_xyz(self):
        self.ud_x()
        self.ud_y()
        self.ud_z()

    def up_t(self):
        self.up_t1()
        self.up_t2()
        self.up_t3()
