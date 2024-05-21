# 实现点动、寸动以及急停
from Delta_robot import DeltaRobotKinematics
# from utils import ws
class ArmController:
    def __init__(self):
        self.robot= DeltaRobotKinematics(390,
                         120,
                         241,
                         300)
        # self.communication = communication
    """
    def cal_ws(self):
        if self.robot.xyz in ws:
            pass
        else:
            return Exception
    """

    # 沿着x轴移动
    def move_arm_x(self, distance):
        self.robot.xyz[0]=self.robot.xyz[0]+distance
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        dt1 = t_new[0]-self.robot.t[0]
        dt2 = t_new[1]-self.robot.t[1]
        dt3 = t_new[2]-self.robot.t[2]
        self.robot.t=t_new
        print(dt1,dt2,dt3)


    # 沿着y轴移动
    def move_arm_y(self, distance):
        self.robot.xyz[1]=self.robot.xyz[1]+distance
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        dt1 = t_new[0]-self.robot.t[0]
        dt2 = t_new[1]-self.robot.t[1]
        dt3 = t_new[2]-self.robot.t[2]
        self.robot.t=t_new
        print(dt1,dt2,dt3)

    # 沿着z轴移动
    def move_arm_z(self, distance):
        self.robot.xyz[2]=self.robot.xyz[2]+distance
        t_new = self.robot.forward_kinematics(self.robot.xyz[0],self.robot.xyz[1],self.robot.xyz[2])
        dt1 = t_new[0]-self.robot.t[0]
        dt2 = t_new[1]-self.robot.t[1]
        dt3 = t_new[2]-self.robot.t[2]
        self.robot.t=t_new
        print(dt1,dt2,dt3)

    # 指定点到点
    def move_arm_w(self, x_n,y_n,z_n):
        t_new = self.robot.forward_kinematics(x_n,y_n,z_n)
        dt1 = t_new[0]-self.robot.t[0]
        dt2 = t_new[1]-self.robot.t[1]
        dt3 = t_new[2]-self.robot.t[2]
        self.robot.t=t_new
        print(dt1,dt2,dt3)

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
