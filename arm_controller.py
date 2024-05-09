# 实现点动、寸动以及急停
class ArmController:
    def __init__(self, communication):
        self.communication = communication

    # 沿着x轴移动
    def move_arm_x(self, distance):
        # 构建移动命令
        command = f"MOVE_X {distance}\n"
        self.send_command(command)

    # 沿着y轴移动
    def move_arm_y(self, distance):
        # 构建移动命令
        command = f"MOVE_Y {distance}\n"
        self.send_command(command)

    # 沿着z轴移动
    def move_arm_z(self, distance):
        # 构建移动命令
        command = f"MOVE_Z {distance}\n"
        self.send_command(command)

    # 指定点到点
    def move_arm_w(self, point):
        # 构建点到点移动命令
        command = f"MOVE_PTP {point['x']} {point['y']} {point['z']}\n"
        self.send_command(command)

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
