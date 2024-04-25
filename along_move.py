import sys
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # 初始化路径不可见
        # self.path_visible = False
        # 初始化路径线
        # self.path_line, = self.ax.plot([], [], [], 'b-', visible=self.path_visible)

    def initUI(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])
        self.ax.set_zlim([0, 1])

        # 末端执行器的点
        self.line, = self.ax.plot([0], [0], [0], 'ro-')

        self.canvas = FigureCanvas(self.fig)
        self.setCentralWidget(self.canvas)

        # 创建水平布局
        hbox = QtWidgets.QHBoxLayout()

        # 创建按钮并添加到水平布局中
        directions = ['X+', 'X-', 'Y+', 'Y-', 'Z+', 'Z-']
        for direction in directions:
            btn = QtWidgets.QPushButton(direction)
            btn.clicked.connect(lambda _, d=direction: self.on_direction_clicked(d))
            hbox.addWidget(btn)

        """
        # 创建显示/隐藏路径的按钮
        self.toggle_path_btn = QtWidgets.QPushButton('Toggle Path')
        self.toggle_path_btn.clicked.connect(self.toggle_path)
        hbox.addWidget(self.toggle_path_btn)
        """


        # 创建一个QWidget对象，将布局添加到其中
        widget = QtWidgets.QWidget()
        widget.setLayout(hbox)

        # 将QWidget对象添加到主窗口的布局中
        self.setMenuWidget(widget)

        self.show()

    def on_direction_clicked(self, direction):
        dx, dy, dz = self.get_movement_from_direction(direction)
        self.update_position(dx, dy, dz)

    def get_movement_from_direction(self, direction):
        if direction == 'X+':
            return 0.1,0,0
        elif direction == 'X-':
            return -0.1, 0, 0
        elif direction == 'Y+':
            return 0, 0.1, 0
        elif direction == 'Y-':
            return 0, -0.1, 0
        elif direction == 'Z+':
            return 0, 0, 0.1
        elif direction == 'Z-':
            return 0, 0, -0.5

    def update_position(self, dx, dy, dz):
        # 更新点的位置
        x, y, z = self.line.get_data_3d()
        new_x, new_y, new_z = x[0] + dx, y[0] + dy, z[0] + dz
        self.line.set_data([new_x], [new_y])
        self.line.set_3d_properties([new_z])
        self.canvas.draw()

        # 更新路径
        # if self.path_visible:
        #   self.update_path(new_x, new_y, 0)

    """

    def update_path(self, x, y, z):
        if not self.path_visible:
            return

        # 获取当前路径线的数据
        px, py, _ = self.path_line.get_data()
        # 追加新点到路径
        self.path_line.set_data(px + [x], py + [y])
        self.path_line.set_3d_properties([z] * len(px) + [z])
        self.canvas.draw()

    def toggle_path(self):
        self.path_visible = not self.path_visible
        self.path_line.set_visible(self.path_visible)
        self.canvas.draw()
        
    """

app = QtWidgets.QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())