import numpy as np
import matplotlib.pyplot as plt

# 设置随机数生成器的种子为0
np.random.seed(0)

R1 = 180  # 静平台的外接圆半径
R2 = 40   # 动平台的外接圆半径
R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径

# 初始化结果数组
xyz = np.array([[0, 0, 0],
                [50, 80, -330],
                [60, 80, -340],
                [60, 80, -330]])

t_results = np.zeros_like(xyz, dtype=object)
v_results = np.zeros((xyz.shape[0]-1, 3))
a_results = np.zeros((xyz.shape[0]-2, 3))

# 静平台半径、动平台半径、杆长等参数
R1 = 180
R2 = 50
R = R1 - R2
l = 270

# 循环遍历xyz数组中的每一行
for i in range(xyz.shape[0]):
    x = xyz[i, 0]
    y = xyz[i, 1]
    z = xyz[i, 2]

    # 建立方程组并计算t1, t2, t3
    t3 = -z - np.sqrt(l**2 - x**2 - (y + R)**2)
    t2 = -z - np.sqrt(l**2 - (x - np.sqrt(3)/2 * R)**2 - (R/2 - y)**2)
    t1 = -z - np.sqrt(l**2 - (np.sqrt(3)/2 * R + x)**2 - (R/2 - y)**2)

    t_results[i] = [t1, t2, t3]

    if i > 0:
        vx = (t_results[i, 0] - t_results[i-1, 0]) / 0.01
        vy = (t_results[i, 1] - t_results[i-1, 1]) / 0.01
        vz = (t_results[i, 2] - t_results[i-1, 2]) / 0.01
        v_results[i-1] = [vx, vy, vz]

    if i > 1:
        zx = (v_results[i-1, 0] - v_results[i-2, 0]) / 0.01
        zy = (v_results[i-1, 1] - v_results[i-2, 1]) / 0.01
        zz = (v_results[i-1, 2] - v_results[i-2, 2]) / 0.01
        a_results[i-2] = [zx, zy, zz]

# 绘制结果
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(xyz.shape[0]):
    x = xyz[i, 0]
    y = xyz[i, 1]
    z = xyz[i, 2]
    ax.scatter(x, y, z, c='b', marker='.')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.grid(True)
ax.axis('equal')

plt.show()
