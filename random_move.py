import sys
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([0, 1])

        self.line, = self.ax.plot([0], [0], [0], 'ro-')  # 末端执行器的点

        self.canvas = FigureCanvas(self.fig)
        self.setCentralWidget(self.canvas)

        # 创建一个按钮并添加到布局中
        self.update_button = QtWidgets.QPushButton('Move Point', self)
        self.update_button.clicked.connect(self.on_button_clicked)
        self.update_button.setGeometry(10, 10, 100, 40)  # 设置按钮的位置和大小
        self.update_button.show()

        self.show()

    def on_button_clicked(self):
        # 随机生成新的x, y, z坐标值
        x, y, z = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 1)
        self.update_position(x, y, z)

    def update_position(self, x, y, z):
        self.line.set_data([x], [y])
        self.line.set_3d_properties([z])
        self.canvas.draw()

app = QtWidgets.QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())