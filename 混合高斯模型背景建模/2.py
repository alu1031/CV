import numpy as np
import cv2

cap = cv2.VideoCapture('test.avi')

# 获取视频信息
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 设置保存视频的编码器和参数
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.avi', fourcc, fps, (width, height))

#形态学操作需要使用的内核
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

#创建混合高斯模型用于背景建模
fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    #形态学开运算去噪点
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    #寻找视频中的轮廓
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for counter in contours:
        #计算各轮廓的周长
        perimeter = cv2.arcLength(counter,True)
        if perimeter > 188:
            #找到一个直矩形（不会旋转）
            x, y, w, h = cv2.boundingRect(counter)
            #画出这个矩形
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    out.write(frame)
    cv2.imshow('Motion Detection',frame)
    cv2.imshow('fgmask', fgmask)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()