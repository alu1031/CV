import cv2
import numpy as np

# 读取视频
cap = cv2.VideoCapture('test.avi')

# 初始化背景模型
background_model = None

# 读取视频帧
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 灰度转换
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 如果没有背景模型，则将当前帧设为初始背景模型
    if background_model is None:
        background_model = gray.copy().astype(float)
        continue
    
    # 更新背景模型（采用累加权重法）
    alpha = 0.01  # 背景更新速率
    cv2.accumulateWeighted(gray, background_model, alpha)
    
    # 计算差值图像
    diff = cv2.absdiff(gray, cv2.convertScaleAbs(background_model))
    
    # 图像去噪
    diff = cv2.medianBlur(diff, 5)
    
    # 二值化处理
    _, thresholded = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # 形态学变换（开运算）
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    
    # 寻找轮廓并绘制候选框
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # 设置最小轮廓面积
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # 显示结果
    cv2.imshow('Motion Detection', frame)
    
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
