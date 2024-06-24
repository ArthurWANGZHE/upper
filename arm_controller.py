# 实现点动、寸动以及急停
from Delta_robot import DeltaRobotKinematics
from communication import Communication
from joblib import dump, load
from camera import camera_still
from camera import camera_vedio
# from utils import ws
#model_filename=""
class ArmController:
    def __init__(self):
        self.robot= DeltaRobotKinematics(390,
                         120,
                         241,
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
        for i in range(len(packages)):
            protocol=self.communication.write(packages[i])
            self.communication.send_data(protocol)
            print(protocol)
            # response = self.communication.receive_data()
            # print(f"接收到返回信息: {response}")

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
        for i in range(len(packages)):
            protocol=self.communication.write(packages[i])
            self.communication.send_data(protocol)
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
        for i in range(len(packages)):
            protocol=self.communication.write(packages[i])
            self.communication.send_data(protocol)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        self.robot.t=t_new
        return

    # 指定点到点
    def move_arm_w(self, x_n,y_n,z_n):
        x1,y1,z1 = self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2]
        x2,y2,z2 = x_n,y_n,z_n
        self.robot.xyz=[x_n,y_n,z_n]
        points, velocity, acceleration, jerk=self.robot.point2point(x1, y1, z1, x2, y2, z2)
        packages=self.communication.packing(points, velocity, acceleration, jerk)
        for i in range(len(packages)):
            protocol=self.communication.write(packages[i])
            self.communication.send_data(protocol)
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        self.robot.t=t_new
        return

    # 急停
    def stop(self):
        # 构建急停命令
        command = "STOP\n"
        self.send_command(command)

    def send_command(self, command):
        if self.communication.serial_thread and self.communication.serial_thread.serial.is_open:
            self.communication.serial_thread.write_data(command)
        else:
            print("串口未打开或发送线程未启动")

    def point2point(self, x1,y1,z1,x2,y2,z2):
        points, velocity, acceleration, jerk=self.robot.point2point(x1, y1, z1, x2, y2, z2)
        return points, velocity, acceleration, jerk

    def classify(self,classifer,classes):
        frame=camera_still()
        pass

    def recieve_data(self):
        self.communication.receive_data()

    def is_connected(self):
        print(self.communication.is_serial_connected())
