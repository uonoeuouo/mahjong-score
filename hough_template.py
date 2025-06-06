import cv2
import numpy as np
import os

def multi_scale_template_matching(image, template, scale_range=(0.5, 2.0), scale_steps=20):
    """
    マルチスケールテンプレートマッチングを実行する関数
    """
    if image is None or template is None:
        print("画像の読み込みに失敗しました")
        return None, None, None
        
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image.copy()
        
    if len(template.shape) == 3:
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    else:
        gray_template = template.copy()
    
    best_score = -np.inf
    best_scale = 1.0
    best_loc = None
    
    h, w = gray_template.shape
    
    # スケールの範囲を確認
    scales = np.linspace(scale_range[0], scale_range[1], scale_steps)
    
    for scale in scales:
        try:
            # テンプレート画像のリサイズ（小数点以下を丸める）
            new_w = max(int(w * scale), 1)
            new_h = max(int(h * scale), 1)
            resized_template = cv2.resize(gray_template, (new_w, new_h), 
                                        interpolation=cv2.INTER_LINEAR)
            
            # 画像サイズの確認
            if resized_template.shape[0] > gray_image.shape[0] or \
               resized_template.shape[1] > gray_image.shape[1]:
                continue
            
            # テンプレートマッチング実行
            result = cv2.matchTemplate(gray_image, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_score:
                best_score = max_val
                best_scale = scale
                best_loc = max_loc
                
        except Exception as e:
            print(f"スケール {scale} でエラーが発生: {str(e)}")
            continue
    
    if best_loc is None:
        print("マッチする結果が見つかりませんでした")
        return None, None, None
        
    return best_score, best_loc, best_scale

def detect_lines_and_template(image_path, template_path, threshold=0.3):
    """
    ハフ変換による直線検出とマルチスケールテンプレートマッチングを実行
    """
    # 画像の存在確認
    if not os.path.exists(image_path) or not os.path.exists(template_path):
        print("指定された画像ファイルが見つかりません")
        return None, None, None, None
    
    # メイン画像の読み込み
    img = cv2.imread(image_path)
    if img is None:
        print(f"画像の読み込みに失敗: {image_path}")
        return None, None, None, None
        
    template = cv2.imread(template_path)
    if template is None:
        print(f"テンプレート画像の読み込みに失敗: {template_path}")
        return None, None, None, None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    try:
        # Cannyエッジ検出
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # ハフ変換で直線検出
        lines = cv2.HoughLinesP(edges,
                              rho=1,
                              theta=np.pi/180,
                              threshold=40,
                              minLineLength=100,
                              maxLineGap=5)
        
        # 直線を描画
        line_img = img.copy()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # マルチスケールテンプレートマッチングの実行
        score, loc, scale = multi_scale_template_matching(img, template)
        
        if score is not None and loc is not None:
            # テンプレートのサイズを取得して、スケールに応じて調整
            h, w = template.shape[:2]
            scaled_w = max(int(w * scale), 1)
            scaled_h = max(int(h * scale), 1)
            
            # 類似度が閾値以上の場合
            if score >= threshold:
                top_left = loc
                bottom_right = (top_left[0] + scaled_w, top_left[1] + scaled_h)
                
                # マッチした場所を赤色の矩形で囲む
                cv2.rectangle(line_img, top_left, bottom_right, (0, 0, 255), 2)
                
                print(f"テンプレートマッチング: 類似度 {score:.2f}, スケール {scale:.2f}")
            else:
                print(f"テンプレートが見つかりませんでした。(類似度: {score:.2f})")
        
        # 結果の表示
        cv2.imshow("Edges", edges)
        cv2.imshow("Lines and Template Match", line_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return line_img, score, loc, scale
        
    except Exception as e:
        print(f"処理中にエラーが発生しました: {str(e)}")
        return None, None, None, None

if __name__ == "__main__":
    # 使用例
    image_path = 'score1.png'
    template_path = 'temp3.png'
    
    # スケール範囲とステップ数を指定してマッチング実行
    result = detect_lines_and_template(
        image_path, 
        template_path,
        threshold=0.3  # マッチング閾値
    )
    
    if result[0] is None:
        print("処理が失敗しました")