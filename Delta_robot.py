import math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import cumtrapz
import numpy as np


class DeltaRobotKinematics:
    def __init__(self, static_dia, moving_dia, link_length, length):
        self.static_dia = static_dia
        self.moving_dia = moving_dia
        self.link_length = link_length
        self.travel_range = (0, length)
        self.base_radius = static_dia / 2  # 静平台半径
        self.top_radius = moving_dia / 2  # 动平台半径
        self.theta = math.radians(120)  # 角度转换为弧度
        self.vmax = 20
        self.amax = 15
        self.jmax = 20
        self.mydt = 0.1
        self.xyz = [0.0, 0.0, -273.92]
        self.t = [0, 0, 0]

    def inverse_kinematics(self, t1, t2, t3):
        """逆运动学：根据滑块距离计算动平台中心坐标"""
        # 定义几何参数
        R1 = self.base_radius  # 静平台的外接圆半径
        R2 = self.top_radius  # 动平台的外接圆半径
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


    def forward_kinematics(self, x, y, z):
        """正运动学：根据动平台中心坐标计算滑块距离"""
        R = self.base_radius - self.top_radius
        l = self.link_length
        t3 = -z - np.sqrt(l ** 2 - x ** 2 - (y + R) ** 2)
        t2 = -z - np.sqrt(l ** 2 - (x - np.sqrt(3) / 2 * R) ** 2 - (R / 2 - y) ** 2)
        t1 = -z - np.sqrt(l ** 2 - (np.sqrt(3) / 2 * R + x) ** 2 - (R / 2 - y) ** 2)

        return [t1, t2, t3]

    def point2point_ss(self, x1, y1, z1, x2, y2, z2):
        # 双s
        P1 = np.array([x1, y1, z1])
        P2 = np.array([x2, y2, z2])

        # 定义几何参数
        R1 = self.base_radius  # 静平台的外接圆半径
        R2 = self.top_radius  # 动平台的外接圆半径
        R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径
        l = self.link_length
        mydt = self.mydt
        vmax = self.vmax
        amax = self.amax
        jmax = self.jmax

        q1 = np.linalg.norm(P2 - P1)
        q0 = 0
        v0 = 0
        v1 = 0
        count = 0
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
                t_results[i] = self.forward_kinematics(x, y, z)

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

    def point2point(self, x1, y1, z1, x2, y2, z2):
        P1 = np.array([float(x1), float(y1), float(z1)])
        P2 = np.array([x2, y2, z2])

        # 定义几何参数
        R1 = self.base_radius  # 静平台的外接圆半径
        R2 = self.top_radius  # 动平台的外接圆半径
        R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径
        l = self.link_length
        mydt = self.mydt
        vmax = self.vmax
        amax = self.amax
        jmax = self.jmax

        q1 = np.linalg.norm(P2 - P1)
        q0 = 0
        v0 = 0
        v1 = 0
        T = math.sqrt(8.135 * q1 / amax)

        # 初始化加速度、速度、位置、时间等数组
        displacement = []
        velocity = []
        acceleration = []
        jerk = []
        points = []

        for t in np.arange(0, T + mydt, mydt):
            # 计算当前时间占总时间的比例
            tao = t / T
            # 根据时间比例计算当前位置、速度、加速度和加加速度
            s = amax / 8.135 * T * T * (20 * tao ** 3 - 45 * tao ** 4 + 36 * tao ** 5 - 10 * tao ** 6)
            v = amax / 8.135 * T * (60 * tao ** 2 - 180 * tao ** 3 + 180 * tao ** 4 - 60 * tao ** 5)
            a = amax / 8.135 * (120 * tao - 540 * tao ** 2 + 720 * tao ** 3 - 300 * tao ** 4)
            j = amax / 8.135 / T * (120 - 1080 * tao + 2160 * tao ** 2 - 1200 * tao ** 3)

            # 将计算结果保存到数组中
            displacement.append(s)
            velocity.append(v)
            acceleration.append(a)
            jerk.append(j)

            if s <= q1:
                scal = s / q1
                p = P1 + (P2 - P1) * scal
                points.append(p)

        # 将结果转换为 numpy 数组

        return points, velocity, acceleration, jerk

    def gate_curve(self):
        # 定义几何参数
        R1 = self.base_radius  # 静平台的外接圆半径
        R2 = self.top_radius  # 动平台的外接圆半径
        R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径
        l = self.link_length
        mydt = self.mydt
        vmax = self.vmax
        amax = self.amax
        jmax = self.jmax

        # 门型点
        P1 = np.array([0, -50, -380])  # 第一个门型点的坐标
        P2 = np.array([0, -50, -355])  # 第二个门型点的坐标
        P3 = np.array([0, -25, -330])  # 第三个门型点的坐标
        P4 = np.array([0, 25, -330])  # 第四个门型点的坐标
        P5 = np.array([0, 50, -355])  # 第五个门型点的坐标
        P6 = np.array([0, 50, -380])  # 第六个门型点的坐标
        P = np.array([P1, P2, P3, P4, P5, P6])  # 将所有门型点组合成一个矩阵

        # 计算各段长度
        s1 = np.linalg.norm(P2 - P1)
        r2 = 25  # 圆弧半径，已知
        s2 = np.pi * r2 / 2  # 四分之一个圆的周长
        s3 = np.linalg.norm(P4 - P3)
        r4 = 25  # 圆弧半径，已知
        s4 = np.pi * r4 / 2  # 四分之一个圆的周长
        s5 = np.linalg.norm(P6 - P5)
        s12345 = s1 + s2 + s3 + s4 + s5

        # 计算运动总时间
        T = np.sqrt(8.135 * s12345 / amax)

        # 初始化加速度、速度、位置、时间等数组
        svajArr = []
        tArr = []
        pArr = []

        for t in np.arange(0, T + mydt, mydt):
            # 计算当前时间占总时间的比例
            tao = t / T
            # 根据时间比例计算当前位置、速度、加速度和加加速度
            s = amax / 8.135 * T ** 2 * (20 * tao ** 3 - 45 * tao ** 4 + 36 * tao ** 5 - 10 * tao ** 6)
            v = amax / 8.135 * T * (60 * tao ** 2 - 180 * tao ** 3 + 180 * tao ** 4 - 60 * tao ** 5)
            a = amax / 8.135 * (120 * tao - 540 * tao ** 2 + 720 * tao ** 3 - 300 * tao ** 4)
            j = amax / 8.135 / T * (120 - 1080 * tao + 2160 * tao ** 2 - 1200 * tao ** 3)

            # 将计算结果保存到数组中
            svajArr.append([s, v, a, j])
            tArr.append(t)

            # 根据当前位置选择对应的门型点
            if s <= s1:
                scal = s / s1
                p = P1 + (P2 - P1) * scal
            elif s <= (s1 + s2):
                # 计算第一段圆弧上的点
                scal = (s - s1) / s2
                angle = -scal * np.pi / 2  # 顺时针方向
                center = np.array([0, -50 + r2, -355])  # 圆心在 yz 平面上
                p = center + r2 * np.array([0, -np.cos(angle), -np.sin(angle)])
            elif s <= (s1 + s2 + s3):
                scal = (s - s1 - s2) / s3
                p = P3 + (P4 - P3) * scal
            elif s <= (s1 + s2 + s3 + s4):
                # 计算第二段圆弧上的点
                scal = (s - s1 - s2 - s3) / s4
                angle = (1 - scal) * np.pi / 2  # 顺时针方向
                center = np.array([0, 50 - r4, -355])  # 圆心在 yz 平面上
                p = center + r4 * np.array([0, np.cos(angle), np.sin(angle)])
            else:
                scal = (s - s1 - s2 - s3 - s4) / s5
                p = P5 + (P6 - P5) * scal

            pArr.append(p)

        svajArr = np.array(svajArr)
        tArr = np.array(tArr)
        pArr = np.array(pArr)

        # 初始化结果数组，大小与 pArr 相同，但每个元素都是一个 3 元素的数组，用于存储 t1, t2, t3
        sz = [len(pArr), 3]  # pArr 的长度和每个点的维度
        m, n = sz
        t_results = [[0] * n for _ in range(m)]  # 创建一个全零数组

        # 循环遍历 pArr 数组中的每一行
        for i in range(m):
            x, y, z = pArr[i]  # 提取每个点的 x, y, z 坐标
            # 存储计算结果
            t_results[i] = [
                (-z - np.sqrt(l ** 2 - x ** 2 - (y + R) ** 2)),
                (-z - np.sqrt(l ** 2 - (x - np.sqrt(3) / 2 * R) ** 2 - (R / 2 - y) ** 2)),
                (-z - np.sqrt(l ** 2 - (np.sqrt(3) / 2 * R + x) ** 2 - (R / 2 - y) ** 2))
            ]

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

        # 输出五个列表
        points = pArr.tolist()
        vc = svajArr[:, 1].tolist()
        ac = svajArr[:, 2].tolist()
        jc = svajArr[:, 3].tolist()

        return points, vc, ac, jc

    def flower(self):

        # 定义几何参数
        R1 = self.base_radius  # 静平台的外接圆半径
        R2 = self.top_radius  # 动平台的外接圆半径
        R = R1 - R2  # 三角锥法后移动到一点后的向xoy投影的三角形的半径
        l = self.link_length
        mydt = self.mydt
        vmax = self.vmax
        amax = self.amax
        jmax = self.jmax


        q0 = 0
        v0 = 0
        v1 = 0

        TT = 100
        bb = np.linspace(0, 2 * np.pi, TT)  # 生成从0到2π的点
        n = 5  # 花瓣的数量
        RR = 25
        r = RR + RR / 2 * np.cos(n * bb)  # 半径方程，控制花瓣的形状

        x = r * np.cos(bb)  # 计算x坐标
        y = r * np.sin(bb)  # 计算y坐标
        z = -380 * np.ones(TT)  # 将z坐标设为常数

        # 创建点坐标数组
        p = np.column_stack((x, y, z))

        # 选择特定点作为控制点
        indices = np.round(np.linspace(0, len(bb) - 1, TT)).astype(int)
        cpts = p[indices, :]

        # 计算每段的长度和总长度
        ds = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2 + np.diff(z) ** 2)
        total_length = np.sum(ds)

        # 时间参数
        tpts = [0, TT * mydt]
        tvec = np.arange(0, TT * mydt + mydt, mydt)

        # 生成B样条轨迹
        # 注意：这里需要一个 bsplinepolytraj 函数的替代，SciPy 中没有直接的函数
        # 这里使用 CubicSpline 作为示例，但可能需要调整以匹配原始 MATLAB 函数的行为
        cs = CubicSpline(tvec, cpts.T, bc_type='periodic')
        q = cs(np.linspace(tvec[0], tvec[-1], int(TT * mydt / mydt + 1)).T)

        # 计算控制点之间的总距离和
        total_distance = np.sum(np.sqrt(np.sum(np.diff(q, axis=1) ** 2, axis=0)))

        # 计算运动总时间
        T = ((total_distance / amax) ** 0.5) * (8.135) ** 0.5

        # 初始化数组
        svajArr = np.zeros((int(T / mydt), 5))  # s, v, a, j
        tArr = np.arange(0, T, mydt)
        pArr = np.zeros((int(T / mydt), 3))

        # 计算运动参数
        for i, t in enumerate(tArr):
            tao = t / T
            s = amax / 8.135 * T ** 2 * (20 * tao ** 3 - 45 * tao ** 4 + 36 * tao ** 5 - 10 * tao ** 6)
            v = amax / 8.135 * T * (60 * tao ** 2 - 180 * tao ** 3 + 180 * tao ** 4 - 60 * tao ** 5)
            a = amax / 8.135 * (120 * tao - 540 * tao ** 2 + 720 * tao ** 3 - 300 * tao ** 4)
            j = amax / 8.135 / T * (120 - 1080 * tao + 2160 * tao ** 2 - 1200 * tao ** 3)
            svajArr[i, :] = [s, v, a, j]
            pArr[i, :] = q[:, i]

        # 插值轨迹点
        p = cs(tArr).T

        # 计算 t1, t2, t3
        for i in range(p.shape[0]):
            x, y, z = p[i, :]
            t3 = -z - np.sqrt(l ** 2 - x ** 2 - (y + R) ** 2)
            t2 = -z - np.sqrt(l ** 2 - (x - np.sqrt(3) / 2 * R) ** 2 - (R / 2 - y) ** 2)
            t1 = -z - np.sqrt(l ** 2 - (np.sqrt(3) / 2 * R + x) ** 2 - (R / 2 - y) ** 2)
            pArr[i, :] = [t1, t2, t3]

        # 计算速度、加速度、加加速度
        velocity = np.diff(pArr, axis=0) / mydt
        acceleration = np.diff(velocity, axis=0) / mydt
        jerk = np.diff(acceleration, axis=0) / mydt

        # 填充首尾使得尺寸匹配
        velocity = np.vstack((velocity, np.zeros((1, 3))))
        acceleration = np.vstack((acceleration, np.zeros((1, 3))))
        jerk = np.vstack((jerk, np.zeros((1, 3))))

        points = pArr.tolist()  # 将点坐标数组转换为列表
        velocity = velocity.tolist()  # 速度数组转换为列表
        acceleration = acceleration.tolist()  # 加速度数组转换为列表
        jerk = jerk.tolist()  # 加加速度数组转换为列表

        return points, velocity, acceleration, jerk

