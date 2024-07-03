import numpy as np
import math

# 输入两个坐标值（单位：mm）
P1 = np.array([-50, -50, -300])
P2 = np.array([0, -50, -380])

# 输入参数
R1 = 125  # 外圆半径
R2 = 60  # 内圆半径
l = 280  # 机械臂长度

# 计算直线插补的距离（单位：mm）
q1 = np.linalg.norm(P1 - P2)  # 位移（单位：mm）

# 运动参数
v_max = 20  # 最大速度（单位：mm/s）
a_max = 15  # 最大加速度（单位：mm/s²）
j_max = 20  # 最大加加速度（单位：mm/s³）
v_initial = 0  # 初始速度（单位：mm/s）
v_final = 0  # 终止速度（单位：mm/s）
dt = 0.1  # 插补步长

# 计算加速度和减速度阶段的时间和位移
T_j1 = math.sqrt((v_max - v_initial) / j_max)
T_a1 = 2 * T_j1
T_j2 = math.sqrt((v_max - v_final) / j_max)
T_a2 = 2 * T_j2

# 计算总时间
T = T_a1 + (q1 - v_max * T_j1) / v_max + (v_max - v_final) / j_max + T_a2

# 计算轨迹
trajectory = []
current_position = P1
current_velocity = np.zeros(3)
current_acceleration = np.zeros(3)
time_elapsed = 0

while time_elapsed < T:
    # 根据时间计算速度和加速度
    if time_elapsed < T_j1:
        current_velocity = v_initial + j_max * time_elapsed
        current_acceleration = j_max
    else:
        current_velocity = v_max
        current_acceleration = 0

    # 更新位置
    displacement = current_velocity * dt + 0.5 * current_acceleration * dt ** 2
    current_position += displacement

    # 更新时间
    time_elapsed += dt

    # 存储结果
    trajectory.append({
        'position': current_position,
        'velocity': current_velocity,
        'acceleration': current_acceleration
    })

# 输出结果
for i, step in enumerate(trajectory):
    print(
        f"Step {i}: Position = {step['position']}, Velocity = {step['velocity']}, Acceleration = {step['acceleration']}")

