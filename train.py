import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump, load
# 假设您已经有了一个包含图片路径和标签的列表
image_paths = [...]  # 图片路径列表
labels = [...]       # 对应的标签列表

# 定义颜色方块的类别
classes = np.unique(labels)

# 读取图片并提取颜色特征
def extract_color_features(image_paths, target_size=(50, 50)):
    features = []
    for path in image_paths:
        # 读取图片
        image = cv2.imread(path)
        # 调整图片大小
        image = cv2.resize(image, target_size)
        # 转换为灰度图，这里为了简化，我们只使用一个颜色通道
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 将图片数据转换为一维数组
        feature_vector = gray.flatten()
        features.append(feature_vector)
    return np.array(features)

# 提取特征
features = extract_color_features(image_paths)
# 将标签转换为独热编码
labels_encoded = np.array([[1 if x == label else 0 for label in classes] for x in labels])

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, labels_encoded, test_size=0.2, random_state=42)

# 创建分类器
classifier = RandomForestClassifier(n_estimators=100)

# 训练模型
classifier.fit(X_train, y_train)

# 预测测试集
y_pred = classifier.predict(X_test)
model_filename = 'color_classifier.joblib'
dump(classifier, model_filename)
print(f"模型已保存到 {model_filename}")
# 评估模型
print(classification_report(y_test, y_pred))

# 应用模型
def classify_new_image(image_path):
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

# 使用模型对新图片进行分类
new_image_path = 'path_to_new_image.jpg'  # 替换为新图片的路径
predicted_class = classify_new_image(new_image_path)
print(f"预测的方块颜色类别是: {predicted_class}")