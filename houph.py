import cv2
import numpy as np

img = cv2.imread('score1.png')  # スクリーンショット全体
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Image", gray)
cv2.waitKey(0)