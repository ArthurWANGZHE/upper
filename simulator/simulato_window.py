# 主窗口界面和布局
from PyQt5.QtWidgets import QMainWindow, QAction, qApp
from simulator.gl_widget import GLWidget

class SimulatorWindow(QMainWindow):
    def __init__(self):
        super(SimulatorWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Delta Robot Simulator')
        self.setGeometry(100, 100, 800, 600)
        self.gl_widget = GLWidget(self)
        self.setCentralWidget(self.gl_widget)

        # 创建菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        view_menu = menubar.addMenu('View')

        # 添加菜单项
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)
        file_menu.addAction(exit_action)

        # 创建状态栏
        self.statusBar().showMessage('Ready')

# 程序入口点
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mainWin = SimulatorWindow()
    mainWin.show()
    sys.exit(app.exec_())
