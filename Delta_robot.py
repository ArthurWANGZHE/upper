import math
import numpy as np

class DeltaRobotKinematics:
    def __init__(self, static_dia, moving_dia, link_length, length):
        self.static_dia = static_dia
        self.moving_dia = moving_dia
        self.link_length = link_length
        self.travel_range = (0,length)
        self.base_radius = static_dia / 2  # 静平台半径
        self.top_radius = moving_dia / 2  # 动平台半径
        self.theta = math.radians(120)  # 角度转换为弧度
        self.xyz=[0.0, 0.0, -273.92]
        self.t=[0,0,0]


    def inverse_kinematics(self, t1, t2, t3):
        """逆运动学：根据滑块距离计算动平台中心坐标"""
        # 定义几何参数
        R1 = self.base_radius  # 静平台的外接圆半径
        R2 = self.top_radius   # 动平台的外接圆半径
        R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径



        # 定义OB, OC, OD
        OB = np.array([-R * math.cos(30 * math.pi / 180), R * math.sin(30 * math.pi / 180), -t2])
        OC = np.array([R * math.cos(30 * math.pi / 180), R * math.sin(30 * math.pi / 180), -t1])
        OD = np.array([0, -R, -t3])
        OB2 = np.array([-R * math.cos(30 * math.pi / 180), R * math.sin(30 * math.pi / 180), 0])
        OC2 = np.array([R * math.cos(30 * math.pi / 180), R * math.sin(30 * math.pi / 180), 0])
        OD2 = np.array([0, -R, 0])
        E = np.array([0, 0, -1])  # 垂直的单位向量
        pmB = np.cross(E, OB2)  # 面法线
        pmC = np.cross(E, OC2)
        pmD = np.cross(E, OD2)

        # 定义AB为杆长
        AB = self.base_radius

        # 计算向量BC和CD
        BC = OC - OB
        CD = OD - OC
        BD = OD - OB

        # 计算OE
        OE = (OB + OC) / 2

        # 计算BE
        lbe = np.linalg.norm(BC) / 2

        # 计算nef
        BCCD = np.cross(BC, CD)
        nef = np.cross(BCCD, BC) / np.linalg.norm(BCCD) / np.linalg.norm(BC)

        # 计算a, b, c
        a = math.sqrt((t3 - t2) ** 2 + (math.sqrt(3) * R) ** 2)
        b = math.sqrt((t2 - t1) ** 2 + (math.sqrt(3) * R) ** 2)
        c = math.sqrt((t3 - t1) ** 2 + (math.sqrt(3) * R) ** 2)

        # 计算p和S
        p = (a + b + c) / 2
        S = math.sqrt(p * (p - a) * (p - b) * (p - c))

        # 计算lbf
        lbf = a * b * c / (4 * S)

        # 计算Lef
        Lef = math.sqrt(lbf ** 2 - lbe ** 2)

        # 计算EF
        EF = Lef * nef

        # 计算Lfa
        Lfa = math.sqrt(AB ** 2 - lbf ** 2)

        # 计算nfa
        nfa = np.cross(BC, CD) / np.linalg.norm(BCCD)

        # 计算FA
        FA = Lfa * nfa

        # 计算OF
        OF = OE + EF

        # 计算OA
        OA = OF + FA

        # 计算向量AB、AC、AD
        AB = OB - OA
        AC = OC - OA
        AD = OD - OA

        # 计算cosbb、coscc、cosdd
        cosbb = np.dot(pmB, AB) / (np.linalg.norm(pmB) * np.linalg.norm(AB))
        coscc = np.dot(pmC, AC) / (np.linalg.norm(pmC) * np.linalg.norm(AC))
        cosdd = np.dot(pmD, AD) / (np.linalg.norm(pmD) * np.linalg.norm(AD))

        # 提取x, y, z坐标
        x = OA[0]
        y = OA[1]
        z = OA[2]

        return x, y, z
    """
    def calculate_workspace(self,  step=1):
        # 计算工作空间
        t1_range, t2_range, t3_range=self.travel_range,self.travel_range,self.travel_range
        workspace = []
        for t1 in np.arange(t1_range[0], t1_range[1], step):
            for t2 in np.arange(t2_range[0], t2_range[1], step):
                for t3 in np.arange(t3_range[0], t3_range[1], step):
                    try:
                        x, y, z = self.inverse_kinematics(t1, t2, t3)
                        workspace.append((x, y, z))
                    except Exception as e:
                        # 如果计算过程中出现错误，跳过这个点
                        continue
        return np.array(workspace)
    """
    def forward_kinematics(self, x, y, z):
        """正运动学：根据动平台中心坐标计算滑块距离"""
        R = self.base_radius - self.top_radius
        l=  self.link_length
        t3 = -z - np.sqrt(l ** 2 - x ** 2 - (y + R) ** 2)
        t2 = -z - np.sqrt(l ** 2 - (x - np.sqrt(3) / 2 * R) ** 2 - (R / 2 - y) ** 2)
        t1 = -z - np.sqrt(l ** 2 - (np.sqrt(3) / 2 * R + x) ** 2 - (R / 2 - y) ** 2)

        return [t1, t2, t3]

    def point2point(self,x1,y1,z1,x2,y2,z2):
        P1 = np.array([x1,y1,z1])
        P2 = np.array([x2,y2,z2])

        # 定义几何参数
        R1 = self.base_radius  # 静平台的外接圆半径
        R2 = self.top_radius  # 动平台的外接圆半径
        R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径

        l = self.link_length
        mydt=0.01

        q0=0
        q1=np.linalg.norm(P2 - P1)
        vmax=20
        amax=15
        v0=0
        v1=0
        jmax=20
        count=0
        if (vmax - v0) * jmax < amax ** 2:
            if v0 > vmax:
                Tj1 = 0
                Ta = 0
                alima = 0
            else:
                Tj1 = math.sqrt((vmax - v0) / jmax)
                Ta = 2 * Tj1
                alima = Tj1 * jmax
        else:
            Tj1 = amax / jmax
            Ta = Tj1 + (vmax - v0) / amax
            alima = amax

        if (vmax - v1) * jmax < amax ** 2:
            Tj2 = math.sqrt((vmax - v1) / jmax)
            Td = 2 * Tj2
            alimd = Tj2 * jmax
        else:
            Tj2 = amax / jmax
            Td = Tj2 + (vmax - v1) / amax
            alimd = amax


        Tv = (q1 - q0) / vmax - Ta / 2 * (1 + v0 / vmax) - Td / 2 * (1 + v1 / vmax)
        if Tv <= 0:
            Tv = 0
            amax_org = amax

            while Ta < 2 * Tj1 or Td < 2 * Tj2:
                count += 1
                amax = amax - amax_org * 0.1
                alima = amax
                alimd = amax

                # 计算delta
                delta = (amax ** 4) / (jmax ** 2) + 2 * (v0 ** 2 + v1 ** 2) + amax * (
                            4 * (q1 - q0) - 2 * amax / jmax * (v0 + v1))

                # 更新Tj1, Ta, Tj2, Td
                Tj1 = amax / jmax
                Ta = (amax ** 2 / jmax - 2 * v0 + math.sqrt(delta)) / (2 * amax)
                Tj2 = amax / jmax
                Td = (amax ** 2 / jmax - 2 * v1 + math.sqrt(delta)) / (2 * amax)
        # 初始化列表
        p = []
        vc = []
        ac = []
        jc = []
        points = []

        # 计算轨迹
        if Tv > 0:
            vlim = vmax
            T = Tv + Ta + Td
        else:
            Tv = 0
            vlim = v0 + (Ta - Tj1) * alima
            T = Tv + Ta + Td

        # 计算直线插补的方向向量
        direction = (np.array(P2) - np.array(P1)) / q1

        # 生成时间列表
        time_values = np.arange(0, T + mydt, mydt)

        for t in time_values:
            q, v, a, j = q0, v0, 0, 0  # 初始化变量

            if t >= 0 and t < Tj1:
                # 段1：加加速度段
                q = q0 + v0 * t + jmax * t ** 3 / 6
                v = v0 + jmax * t ** 2 / 2
                a = jmax * t
                j = jmax
            elif t >= Tj1 and t < Ta - Tj1:
                # 段2：匀加速度段
                q = q0 + v0 * t + alima / 6 * (3 * t ** 2 - 3 * Tj1 * t + Tj1 ** 2)
                v = v0 + alima * (t - Tj1 / 2)
                a = alima
                j = 0
            elif t >= Ta - Tj1 and t < Ta:
                # 段3：减加速度段
                q = q0 + (vlim + v0) * Ta / 2 - vlim * (Ta - t) + jmax * (Ta - t) ** 3 / 6
                v = vlim - jmax * (Ta - t) ** 2 / 2
                a = jmax * (Ta - t)
                j = -jmax
            elif t >= Ta and t < Ta + Tv:
                # 段4：匀速段
                q = q0 + (vlim + v0) * Ta / 2 + vlim * (t - Ta)
                v = vlim
                a = 0
                j = 0
            elif t >= Ta + Tv and t < T - Td + Tj2:
                # 段5：减加速度段
                q = q1 - (vlim + v1) * Td / 2 + vlim * (t - T + Td) - jmax * (t - T + Td) ** 3 / 6
                v = vlim - jmax * (t - T + Td) ** 2 / 2
                a = -jmax * (t - T + Td)
                j = -jmax
            elif t >= T - Td + Tj2 and t < T - Tj2:
                # 段6：匀减速度段
                q = q1 - (vlim + v1) * Td / 2 + vlim * (t - T + Td) - alimd / 6 * (
                            3 * (t - T + Td) ** 2 - 3 * Tj2 * (t - T + Td) + Tj2 ** 2)
                v = vlim - alimd * (t - T + Td - Tj2 / 2)
                a = -alimd
                j = 0
            elif t >= T - Tj2 and t <= T:
                # 段7：减减速度段
                q = q1 - v1 * (T - t) - jmax * (T - t) ** 3 / 6
                v = v1 + jmax * (T - t) ** 2 / 2
                a = -jmax * (T - t)
                j = jmax

            # 将位置向量投影到三维空间
            pos = P1 + q * direction
            pos = pos.tolist()
            points.append(pos)
            p.append(q)
            vc.append(v)
            ac.append(a)
            jc.append(j)

            sz = [len(points), 3]  # points的长度和每个点的维度
            m, n = sz
            t_results = [[0] * n for _ in range(m)]  # 创建一个全零数组

            # 循环遍历points数组中的每一行
            for i in range(m):
                x, y, z = points[i]  # 提取每个点的x, y, z坐标
                # 存储计算结果
                t_results[i] = self.forward_kinematics(x,y,z)

            # 显示结果（可选）
            # 初始化位移、速度、加速度和加加速度的数组
            displacement = t_results
            velocity = [[0] * n for _ in range(m)]
            acceleration = [[0] * n for _ in range(m)]
            jerk = [[0] * n for _ in range(m)]

            # 计算速度
            for i in range(1, m - 1):
                velocity[i] = [(displacement[i + 1][j] - displacement[i - 1][j]) / (2 * mydt) for j in range(n)]

            # 计算加速度
            for i in range(2, m - 2):
                acceleration[i] = [(velocity[i + 1][j] - velocity[i - 1][j]) / (2 * mydt) for j in range(n)]

            # 计算加加速度
            for i in range(3, m - 3):
                jerk[i] = [(acceleration[i + 1][j] - acceleration[i - 1][j]) / (2 * mydt) for j in range(n)]


        return points, vc, ac, jerk