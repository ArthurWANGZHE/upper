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
        self.xyz=[0.0, -1.4210854715202004e-14, -440.7124727947029]
        self.t=[300,300,300]


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
    def calculate_workspace(self,  step=1):
        """计算工作空间"""
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
    def forward_kinematics(self, x, y, z):
        """正运动学：根据动平台中心坐标计算滑块距离"""
        R = self.base_radius - self.top_radius
        l=  self.link_length
        t3 = -z - np.sqrt(l ** 2 - x ** 2 - (y + R) ** 2)
        t2 = -z - np.sqrt(l ** 2 - (x - np.sqrt(3) / 2 * R) ** 2 - (R / 2 - y) ** 2)
        t1 = -z - np.sqrt(l ** 2 - (np.sqrt(3) / 2 * R + x) ** 2 - (R / 2 - y) ** 2)

        return [t1, t2, t3]


