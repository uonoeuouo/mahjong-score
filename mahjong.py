from PIL import Image
from google.cloud import vision
import io

# サービスアカウントキーのパスを指定
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mahjong-score-461302-205f61b0439b.json"

# クライアントを作成
client = vision.ImageAnnotatorClient()

# 画像を開く
img = Image.open("score1.png")
width, height = img.size

# 相対座標で定義
regions = {
    "1st_name" : (0.510, 0.150, 0.660, 0.200), #(left, top, right, bottom)
    "1st_score" : (0.680, 0.200, 0.780, 0.300),
    "2nd_name" : (0.550, 0.380, 0.700, 0.450),
    "2nd_score" : (0.700, 0.400, 0.780, 0.500),
    "3rd_name" : (0.600, 0.550, 0.730, 0.600),
    "3rd_score" : (0.750, 0.600, 0.800, 0.700),
    "4th_name" : (0.650, 0.750, 0.780, 0.800),
    "4th_score" : (0.780, 0.800, 0.840, 0.880)
}

results = {}
for label, (left_r, top_r, right_r, bottom_r) in regions.items():
    # 実際の座標に変換
    box = (
        int(left_r * width),
        int(top_r * height),
        int(right_r * width),
        int(bottom_r * height)
    )
    cropped = img.crop(box)

    buf = io.BytesIO()
    cropped = cropped.convert("RGB")
    cropped.save(buf, format="JPEG")
    content = buf.getvalue()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    if response.text_annotations:
        results[label] = response.text_annotations[0].description.strip()
    else:
        results[label] = None

# 結果を表示
for label, text in results.items():
    if text:
        print(f"{label}: {text}")
    else:
        print(f"{label}: 認識できませんでした")
