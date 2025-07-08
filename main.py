from new_matching import detect_lines, lines_to_mask, multi_scale_match, process_images
from pick_string import pick_strings

if __name__ == "__main__":
    # 画像処理の実行
    input_image_path = 'score4.png'
    template_image_path = 'temp3.png'
    
    input_color, template_bin, input_bin, cropped_match = process_images(input_image_path, template_image_path)
    
    # 文字列抽出の実行
    pick_strings()