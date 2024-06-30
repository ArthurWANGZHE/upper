# 实现点动、寸动以及急停
from Delta_robot import DeltaRobotKinematics
from communication import Communication
from joblib import dump, load
from camera import camera_still
from camera import camera_vedio
import time
# from utils import ws
#model_filename=""
class ArmController:
    def __init__(self):
        self.robot= DeltaRobotKinematics(133,
                         60,
                         251,
                         300)
        self.communication = Communication()
        #classifier = load(model_filename)

    """
    def cal_ws(self):
        if self.robot.xyz in ws:
            pass
        else:
            return Exception
    """

    # 沿着x轴移动
    def move_arm_x(self, distance):
        x1,y1,z1 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        self.robot.xyz[0]=self.robot.xyz[0]+distance
        x2,y2,z2 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        points, velocity, acceleration, jerk=self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages=self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        self.robot.t=t_new
        return



    # 沿着y轴移动
    def move_arm_y(self, distance):
        x1,y1,z1 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        self.robot.xyz[1]=self.robot.xyz[1]+distance
        x2,y2,z2 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        points, velocity, acceleration, jerk=self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages=self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        self.robot.t=t_new
        return

    # 沿着z轴移动
    def move_arm_z(self, distance):
        x1,y1,z1 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        self.robot.xyz[2]=self.robot.xyz[2]+distance
        x2,y2,z2 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        points, velocity, acceleration, jerk=self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages=self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        self.robot.t=t_new
        return

    # 指定点到点
    def move_arm_2p(self, x_n,y_n,z_n):
        x1,y1,z1 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        x2,y2,z2 = x_n,y_n,z_n
        self.robot.xyz=[x_n,y_n,z_n]
        points, velocity, acceleration, jerk=self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages=self.communication.packing(points, velocity, acceleration, jerk)
        self.communication.send_package(packages)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        self.robot.t=t_new
        return

    def move_gate_curve(self):
        # 归零
        #ff0x02fe
        # 门型曲线
        points, velocity, acceleration, jerk=self.robot.gate_curve()
        packages=self.communication.packing(points, velocity, acceleration)
        self.communication.send_package(packages)

    # 急停
    def stop(self):
        # 构建急停命令
        command = "STOP\n"
        self.send_command(command)


    def point2point(self, x1,y1,z1,x2,y2,z2):
        points, velocity, acceleration, jerk=self.robot.point2point(x1, y1, z1, x2, y2, z2)
        return points, velocity, acceleration, jerk


