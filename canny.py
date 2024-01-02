import cv2


# 對影片做預處理
def cannyEdgeDetector(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 先將影像轉灰階
    blurred = cv2.GaussianBlur(gray, (7, 7), 1.41)  # 去模糊化
    edged = cv2.Canny(blurred, 25, 75)  # 使用 Canny() 方法產生邊緣偵測的影像

    return edged
