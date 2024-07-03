# 三维视图集成OpenGL渲染
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

    def initializeGL(self):
        # 设置背景颜色为黑色
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)  # 启用深度测试

    def resizeGL(self, width, height):
        # 设置视口大小
        glViewport(0, 0, width, height)

    def paintGL(self):
        # 清除颜色缓冲区和深度缓冲区
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 设置当前绘制颜色为白色
        glColor3f(1.0, 1.0, 1.0)

        # 开始绘制三角形
        glBegin(GL_TRIANGLES)
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glEnd()

        # 强制完成所有OpenGL命令
        glFlush()
