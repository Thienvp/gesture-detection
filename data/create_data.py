"""
Bước 1. Đổi các biến : label (nhãn cần thu thập dữ liệu), farmer (tên người thực hiện)
Bước 2. Chạy code
Bước 3. Xem ảnh mẫu trong các folder data để xem dáng tay
Bước 4. Sau khi thực hiện dáng tay xong thì ấn phím 'r' để bắt đầu record. Sau khi record đủ 200 ảnh thì code tự exit.
        Lưu ý: xoay  cổ tay hoặc di chuyển tay một chút để tạo sự đa dạng cho dữ liệu
Bước 5: commit
Bước 6: nhắn vào nhóm "Đã xong"
"""

import math
import os

import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 200

# Change only here
label = "stop"  # left / right / up / stop
farmer = "thien"  # Replace by your NAME
# End changeable Section

record = False
counter = 0
while True:
    success, img = cap.read()
    if not success:
        print("Error: can not get image!!")
        break
    img = cv2.flip(img, 1)
    hand, img = detector.findHands(img)
    if hand:
        hand = hand[0]
        x, y, w, h = hand['bbox']
        imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]
        imgCrop = cv2.flip(imgCrop, 1)

        if imgCrop is not None:
            if h / w > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgCrop = cv2.resize(imgCrop, (wCal, imgSize))
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgCrop = cv2.resize(imgCrop, (imgSize, hCal))
            cv2.imshow("Cropped Image", imgCrop)
            if record:
                path = os.path.join(label, f"{farmer}-{label}-{counter}.jpg")
                print(path)
                cv2.imwrite(path, imgCrop)
                counter += 1
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("e") or counter >= 200:
        exit(0)
    if cv2.waitKey(1) == ord("r"):
        record = True
