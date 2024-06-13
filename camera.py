import cv2
import numpy as np
labels = [...]

# 定义颜色方块的类别
classes = np.unique(labels)
def camera_vedio():
    # 选择摄像头的编号
    cap = cv2.VideoCapture(1)
    # 添加这句是可以用鼠标拖动弹出的窗体
    cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)
    while(cap.isOpened()):
        # 读取摄像头的画面
        ret, frame = cap.read()
        # 真实图
        cv2.imshow('real_img', frame)
        # 按下'q'就退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放画面
    cap.release()
    cv2.destroyAllWindows()

def camera_still():
    # 创建视频捕获对象
    cap = cv2.VideoCapture(0)  # 参数0通常表示默认摄像头

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 读取一帧图像
    ret, frame = cap.read()
    return frame

def classify_new_image(classifier,classes,image_path):
    # 读取新图片
    new_image = cv2.imread(image_path)
    new_image = cv2.resize(new_image, (50, 50))
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    feature_vector = gray.flatten()
    # 预测
    prediction = classifier.predict([feature_vector])
    # 将预测结果转换为人类可读的标签
    predicted_class = classes[np.argmax(prediction)]
    return predicted_class