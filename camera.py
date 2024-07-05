import numpy as np
from PyQt5.Qt import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
import cv2
import time

# 加载模板图像，可以是彩色的
template1 = cv2.imread('yellow.png')
template2 = cv2.imread('red.png')

# 转换为灰度图像
template1 = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
template2 = cv2.cvtColor(template2, cv2.COLOR_BGR2GRAY)
class Camera(QObject):
    sendPicture = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.timer = QTimer()
        self.init_timer()
        self.cap = cv2.VideoCapture()
        self.camera_num = 0


    def init_timer(self):
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.display)

    def set_cam_number(self, n):
        self.camera_num = n

    def open_camera(self):
        print("in open_camera")
        self.cap.set(4, 480)
        self.cap.set(3, 640)
        self.cap.open(self.camera_num)
        self.timer.start()
        # 加载模板图像，可以是彩色的
        template1 = cv2.imread('yellow.png')
        template2 = cv2.imread('red.png')

        # 转换为灰度图像
        self.template1 = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
        self.template2 = cv2.cvtColor(template2, cv2.COLOR_BGR2GRAY)
        self.thread.start()

    def close_camera(self):
        self.cap.release()

    def match_template(self,image, template):
        MIN_MATCH_COUNT = 10


        target=image
        target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)

        # Create a pyramid for the target image
        target_pyr = [target]


        sift = cv2.SIFT_create()

        # Choose the level of the pyramid to perform feature detection and matching

        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(target, None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=30)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            h, w = template.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            # Scale the coordinates of the corners back to the original size

            target = target_pyr[0]  # Use the original size target image
            target = cv2.polylines(target, [np.int32(dst)], True, (255, 0, 0), 3, cv2.LINE_AA)


            draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=None,
                           matchesMask=matchesMask,
                           flags=2)

            result = cv2.drawMatches(template, kp1, target, kp2, good, None, **draw_params)
        else:
            result = image


        return result

    def display(self):
        flag, image = self.cap.read()
        # time.sleep(0.5) # 耗时操作
        image = self.match(image)
        image = self.match(image)
        showImage = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                                 QtGui.QImage.Format_RGB888).rgbSwapped()
        self.sendPicture.emit(showImage)

    def match(self,image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 定义红色和黄色的HSV范围
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])

        # 创建红色和黄色的掩码
        mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        #mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        # 合并红色掩码
        mask_red = mask_red1

        # 寻找红色和黄色区域的轮廓
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c=0
        t=0
        # 绘制图形
        for contour in contours_red:

            if c>=3:
                break

            # 计算轮廓的几何中心
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # 在中心画一个空心的蓝色圆
                cv2.circle(image, (cX, cY), 20, (255, 0, 0), 2)
                c+=1# 蓝色为(255, 0, 0)在BGR

        for contour in contours_yellow:
            if t>=3:
                break
            # 计算轮廓的几何中心
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # 定义三角形的三个点
                triangle = np.array([[[cX - 20, cY], [cX + 20, cY], [cX, cY - 40]]], dtype=np.int32)
                # 在中心画一个空心的蓝色三角形
                # cv2.fillPoly(image, triangle, (255, 255, 255))  # 空心即为白色(255, 255, 255)
                cv2.polylines(image, triangle, True, (255, 0, 0), 2)  # 蓝色边
                t+=1


        # 如果没有检测到颜色，返回原图像
        if len(contours_red) == 0 and len(contours_yellow) == 0:
            return image

        return image


