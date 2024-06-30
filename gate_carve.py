
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

