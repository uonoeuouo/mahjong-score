import cv2
import numpy as np

# 大きな画像（対象）とテンプレート画像（探す対象）を読み込み
img = cv2.imread('score1.png')  # スクリーンショット全体
template = cv2.imread('temp3.png')  # 名前欄だけを切り取った画像

# テンプレートのサイズを取得
w, h = template.shape[1], template.shape[0]

# グレースケールに変換（計算効率向上）
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# テンプレートマッチング実行（類似度を取得）
res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# 類似度の高い場所を取得（max_val: 類似度, max_loc: 座標）
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# 類似度が高ければ OK（例：0.8以上）
if max_val >= 0.5:
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # マッチした場所を矩形で囲む
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    cv2.imshow("Matched Result", img)
    cv2.waitKey(0)
else:
    print("テンプレートが見つかりませんでした。")