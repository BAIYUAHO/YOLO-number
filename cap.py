import os
import cv2
import numpy as np
cap = cv2.VideoCapture(0)# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:    # 逐帧捕获图像
    ret, frame = cap.read()

    # 如果图像获取成功
    if ret:
        # 在窗口中显示图像
        cv2.imshow('Frame', frame)

    # 按下'q'键退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
