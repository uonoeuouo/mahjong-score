import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('score1.png')  # スクリーンショット全体
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # グレースケール画像の表示
# plt.figure(figsize=(10, 5))
# plt.subplot(121)
# plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
# plt.title('original grayscale image')

# # ヒストグラムの表示
# plt.subplot(122)
# plt.hist(gray.flatten(), bins=128)
# plt.xlabel("intensity")
# plt.ylabel("frequency")
# plt.title('histogram')

# # 結果の保存と表示
# plt.tight_layout()  # サブプロットの配置を調整
# plt.savefig('histogram.pdf')  # ヒストグラムを保存
# plt.show()

# Cannyエッジ検出を追加
edges = cv2.Canny(gray, 15, 80, apertureSize=3)

# HoughLinesPのパラメータを調整
lines = cv2.HoughLinesP(edges,
                      rho=1,
                      theta=np.pi/180,  # 角度の分解能を1度に変更
                      threshold=40,    # 投票の閾値を下げて調整
                      minLineLength=100,# 最小線分長を調整
                      maxLineGap=5)     # ギャップを小さく

# 直線を描画
line_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

template = cv2.imread('temp3.png')  # 名前欄だけを切り取った画像
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
(tH, tW) = template_gray.shape[:2]

# マルチスケールテンプレートマッチングの実行
found = None
for scale in np.linspace(0.2, 1.0, 20)[::-1]:
    resized = cv2.resize(line_img, (int(line_img.shape[1]), int(line_img.shape[0] * scale)))
    r = line_img.shape[1] / float(resized.shape[1])
    
    if resized.shape[0] < tH or resized.shape[1] < tW:
        break

    gray_resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    result = cv2.matchTemplate(gray_resized, template_gray, cv2.TM_CCOEFF_NORMED)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    
    if found is None or maxVal > found[0]:
        found = (maxVal, maxLoc, r)

(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)

# エッジ検出結果も表示
cv2.imwrite("output_result.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()