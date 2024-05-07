# gl_widget.py
from PyQt5.QtWidgets import QOpenGLWidget

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

    def initializeGL(self):
        # 在这里初始化OpenGL渲染环境
        pass

    def resizeGL(self, width, height):
        # 在这里响应OpenGL窗口的大小变化
        pass

    def paintGL(self):
        # 在这里执行OpenGL的绘制操作
        pass
