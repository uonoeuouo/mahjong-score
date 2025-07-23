from PIL import Image
from google.cloud import vision
from dotenv import load_dotenv
import config
import discord
import io
import os
import numpy as np
import cv2

def pick_strings():
    load_dotenv()
    credential_path = config.GOOGLE_APPLICATION_CREDENTIALS

    if credential_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
    else:
        raise Exception("GOOGLE_APPLICATION_CREDENTIALS is not set.")


    # クライアントを作成
    client = vision.ImageAnnotatorClient()

    # 画像を開く
    img = Image.open("cropped_match.png")
    width, height = img.size

    # 相対座標で定義
    regions = {
        "1st_name" : (0.260, 0.020, 0.550, 0.100), #(left, top, right, bottom)
        "1st_score" : (0.260, 0.100, 0.500, 0.250),
        "2nd_name" : (0.350, 0.300, 0.600, 0.380),
        "2nd_score" : (0.350, 0.380, 0.550, 0.500),
        "3rd_name" : (0.430, 0.550, 0.700, 0.620),
        "3rd_score" : (0.430, 0.620, 0.650, 0.720),
        "4th_name" : (0.500, 0.780, 0.780, 0.850),
        "4th_score" : (0.500, 0.850, 0.700, 0.950)
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

    # regionの位置を画像に描画
    draw_img = img.convert("RGB")
    draw_img = np.array(draw_img)
    for label, (left_r, top_r, right_r, bottom_r) in regions.items():
        box = (
            int(left_r * width),
            int(top_r * height),
            int(right_r * width),
            int(bottom_r * height)
        )
        cv2.rectangle(draw_img, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
        cv2.putText(draw_img, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # 描画結果を保存
    cv2.imwrite("regions_output.png", draw_img)


if __name__ == "__main__":
    pick_strings()