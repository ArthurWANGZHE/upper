import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 初始化
x = np.zeros((68*68*68,1))
y = np.zeros((68*68*68,1))
z = np.zeros((68*68*68,1))
m = 1

def Delta_Inversesolution(t1, t2, t3):
    R1 = 125  # 静平台的外接圆半径
    R2 = 60  # 动平台的外接圆半径
    R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径

    OB = np.array([-R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), -t2])
    OC = np.array([R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), -t1])
    OD = np.array([0, -R, -t3])
    OB2 = np.array([-R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), 0])
    OC2 = np.array([R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), 0])
    OD2 = np.array([0, -R, 0])
    E = np.array([0, 0, -1])  # 垂直的单位向量
    pmB = np.cross(E, OB2)  # 面法线
    pmC = np.cross(E, OC2)  # 面法线
    pmD = np.cross(E, OD2)  # 面法线

    # 定义AB为杆长
    AB = 280

    # 计算向量BC和CD
    BC = OC - OB
    CD = OD - OC
    BD = OD - OB

    # 计算OE
    OE = (OB + OC) / 2

    # 计算BE
    lbe = np.linalg.norm(BC) / 2

    # 计算nef，即BC和CD的叉积的叉积
    BCCD = np.cross(BC, CD)
    nef = np.cross(BCCD, BC) / np.linalg.norm(BCCD) / np.linalg.norm(BC)

    # 计算a, b, c（注意这里将角度转换为弧度）
    a = np.sqrt((t3 - t2) ** 2 + (np.sqrt(3) * R) ** 2)
    b = np.sqrt((t2 - t1) ** 2 + (np.sqrt(3) * R) ** 2)
    c = np.sqrt((t3 - t1) ** 2 + (np.sqrt(3) * R) ** 2)

    # 计算p和S
    p = (a + b + c) / 2
    S = np.sqrt(p * (p - a) * (p - b) * (p - c))

    # 这里BF似乎是一个错误，应该是lbf
    lbf = a * b * c / (4 * S)

    # 计算Lef
    Lef = np.sqrt(lbf ** 2 - lbe ** 2)

    # 计算EF
    EF = Lef * nef

    Lfa = np.sqrt(AB ** 2 - lbf ** 2)

    # 计算nfa
    nfa = np.cross(BC, CD) / np.linalg.norm(BCCD)

    # 计算FA
    FA = Lfa * nfa

    # 计算OF
    OF = OE + EF

    # 计算OA
    OA = OF + FA
    AB = OB - OA
    AC = OC - OA
    AD = OD - OA
    cosbb = np.dot(pmB, AB) / (np.linalg.norm(pmB) * np.linalg.norm(AB))  # 角度值
    coscc = np.dot(pmC, AC) / (np.linalg.norm(pmC) * np.linalg.norm(AC))  # 角度值
    cosdd = np.dot(pmD, AD) / (np.linalg.norm(pmD) * np.linalg.norm(AD))  # 角度值

    # 提取x, y, z坐标
    x = OA[0]
    y = OA[1]
    z = OA[2]

    return x, y, z


def Delta_Inversesolution2(t1, t2, t3):
    R1 = 125  # 静平台的外接圆半径
    R2 = 60  # 动平台的外接圆半径
    R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径

    OB = np.array([-R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), -t2])
    OC = np.array([R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), -t1])
    OD = np.array([0, -R, -t3])
    OB2 = np.array([-R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), 0])
    OC2 = np.array([R * np.cos(30 * np.pi / 180), R * np.sin(30 * np.pi / 180), 0])
    OD2 = np.array([0, -R, 0])
    E = np.array([0, 0, -1])  # 垂直的单位向量
    pmB = np.cross(E, OB2)  # 面法线
    pmC = np.cross(E, OC2)  # 面法线
    pmD = np.cross(E, OD2)  # 面法线

    # 定义AB为杆长
    AB = 280

    # 计算向量BC和CD
    BC = OC - OB
    CD = OD - OC
    BD = OD - OB

    # 计算OE
    OE = (OB + OC) / 2

    # 计算BE
    lbe = np.linalg.norm(BC) / 2

    # 计算nef，即BC和CD的叉积的叉积
    BCCD = np.cross(BC, CD)
    nef = np.cross(BCCD, BC) / np.linalg.norm(BCCD) / np.linalg.norm(BC)

    # 计算a, b, c（注意这里将角度转换为弧度）
    a = np.sqrt((t3 - t2) ** 2 + (np.sqrt(3) * R) ** 2)
    b = np.sqrt((t2 - t1) ** 2 + (np.sqrt(3) * R) ** 2)
    c = np.sqrt((t3 - t1) ** 2 + (np.sqrt(3) * R) ** 2)

    # 计算p和S
    p = (a + b + c) / 2
    S = np.sqrt(p * (p - a) * (p - b) * (p - c))

    # 这里BF似乎是一个错误，应该是lbf
    lbf = a * b * c / (4 * S)

    # 计算Lef
    Lef = np.sqrt(lbf ** 2 - lbe ** 2)

    # 计算EF
    EF = Lef * nef

    Lfa = np.sqrt(AB ** 2 - lbf ** 2)

    # 计算nfa
    nfa = np.cross(BC, CD) / np.linalg.norm(BCCD)

    # 计算FA
    FA = Lfa * nfa

    # 计算OF
    OF = OE + EF

    # 计算OA
    OA = OF + FA
    AB = OB - OA
    AC = OC - OA
    AD = OD - OA
    cosbb = np.dot(pmB, AB) / (np.linalg.norm(pmB) * np.linalg.norm(AB))  # 角度值
    coscc = np.dot(pmC, AC) / (np.linalg.norm(pmC) * np.linalg.norm(AC))  # 角度值
    cosdd = np.dot(pmD, AD) / (np.linalg.norm(pmD) * np.linalg.norm(AD))  # 角度值

    return cosbb, coscc, cosdd


# 遍历三维空间并绘制原始工作空间和裁剪后的工作空间
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(1, 301, 2):
    for j in range(1, 301, 2):
        for k in range(1, 301, 2):
            [cosb, cosc, cosd] = Delta_Inversesolution2(k, j, i)
            [x1, y1, z1] = Delta_Inversesolution(k, j, i)
            if (abs(cosb) < 0.34 and abs(cosc) < 0.34 and abs(cosd) < 0.34 and z1 > -430):
                # 绘制原始工作空间
                ax.scatter3D(x1, y1, z1, c='r', alpha=0.1)
                # 六棱柱的条件
                if abs(y1) < np.sqrt(3) * (150 - abs(x1)):
                    m += 1
                    x[m] = x1
                    y[m] = y1
                    z[m] = z1
# 绘制裁剪后的工作空间
ax.scatter3D(x[:m], y[:m], z[:m], c=x[:m], cmap='jet')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Original and Trimmed Workspace')
plt.show()

# 输出X，Y，Z的范围
print("X range: ", np.min(x[:m]), "to", np.max(x[:m]))
print("Y range: ", np.min(y[:m]), "to", np.max(y[:m]))
print("Z range: ", np.min(z[:m]), "to", np.max(z[:m]))
