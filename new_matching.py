import cv2
import numpy as np
import matplotlib.pyplot as plt

# 直線検出
def detect_lines(image, min_length=100, canny1=50, canny2=150):
    edges = cv2.Canny(image, canny1, canny2)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180,
                            threshold=100, minLineLength=min_length, maxLineGap=10)
    return lines

# ラスタライズ（線を2値画像化
def lines_to_mask(image_shape, lines, thickness=3):
    mask = np.zeros(image_shape, dtype=np.uint8)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(mask, (x1, y1), (x2, y2), 255, thickness=thickness)
    return mask

# マルチスケールマッチング（2値画像同士）
def multi_scale_match(input_bin, template_bin, scales=np.linspace(0.8, 1.2, 20)):
    results = []
    for scale in scales:
        resized_template = cv2.resize(template_bin, None, fx=scale, fy=scale)
        th, tw = resized_template.shape

        if th > input_bin.shape[0] or tw > input_bin.shape[1]:
            continue

        result = cv2.matchTemplate(input_bin, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        results.append({
            'score': max_val,
            'top_left': max_loc,
            'w': tw,
            'h': th,
            'scale': scale
        })

    if not results:
        return None
    return max(results, key=lambda r: r['score'])

def process_images(input_image_path, template_image_path):
    # 入力とテンプレート画像の読み込み
    template_gray = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
    image_array = np.frombuffer(input_image_path.read(), dtype=np.uint8)
    input_gray = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)
    input_color = cv2.cvtColor(input_gray, cv2.COLOR_GRAY2BGR)

    # テンプレート画像の高さを入力画像の80%にリサイズ
    input_height = input_gray.shape[0]
    template_height, template_width = template_gray.shape
    target_height = int(input_height * 0.8)
    scale_factor = target_height / template_height
    target_width = int(template_width * scale_factor)
    template_gray = cv2.resize(template_gray, (target_width, target_height))

    # 直線検出
    lines_template = detect_lines(template_gray, min_length=30)
    lines_input = detect_lines(input_gray, min_length=100)

    # ラスタライズ（2値画像）
    template_bin = lines_to_mask(template_gray.shape, lines_template, thickness=3)
    input_bin = lines_to_mask(input_gray.shape, lines_input, thickness=3)

    # ガウシアンブラーを適用
    template_bin = cv2.GaussianBlur(template_bin, (5, 5), sigmaX=1.0)
    input_bin = cv2.GaussianBlur(input_bin, (5, 5), sigmaX=1.0)

    # マルチスケールマッチング
    top_match = multi_scale_match(input_bin, template_bin)

    # マッチ結果描画
    cropped_match = None
    if top_match:
        x, y = top_match['top_left']
        w, h = top_match['w'], top_match['h']
        cv2.rectangle(input_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(input_color, f"Top1 (scale={top_match['scale']:.2f})", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # 矩形部分をトリミングして別の変数に保存
        cropped_match = input_color[y:y+h, x:x+w]
        cv2.imwrite('cropped_match.png', cropped_match)

    return input_color, template_bin, input_bin, cropped_match

if __name__ == "__main__":
    input_image_path = 'score2.png'
    template_image_path = 'temp3.png'

    # 関数を呼び出して処理を実行
    input_color, template_bin, input_bin, cropped_match = process_images(input_image_path, template_image_path)

    # # 可視化
    # plt.figure(figsize=(18, 6))

    # plt.subplot(1, 3, 1)
    # plt.imshow(template_bin, cmap='gray')
    # plt.title('Template Mask (Blurred)')
    # plt.axis('off')

    # plt.subplot(1, 3, 2)
    # plt.imshow(input_bin, cmap='gray')
    # plt.title('Input Mask (Blurred)')
    # plt.axis('off')

    # plt.subplot(1, 3, 3)
    # plt.imshow(cv2.cvtColor(input_color, cv2.COLOR_BGR2RGB))
    # plt.title('Match Result')
    # plt.axis('off')

    # plt.tight_layout()
    # plt.show()
