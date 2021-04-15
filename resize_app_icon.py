import copy
import os

from PIL import Image, ImageDraw

path = "/Users/clj/Pictures/icon/Ximind.png"  # 大于等于512x512的直角大图
androidIconSize = [96, 144, 192]
# androidNames = ['mipmap-xhdpi', 'mipmap-xxhdpi', 'mipmap-xxxhdpi']
androidNames = ['x2', 'x3', 'x4']


# 处理图片圆角
def circle_corner(image, radii):
    temp_file = copy.copy(image)
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    (w, h) = temp_file.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', temp_file.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()

    temp_file.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return temp_file


# 生成Android的icon
def create_android_icon(image_path):
    img_dir = os.path.dirname(image_path)
    # 获取图片
    img_file = Image.open(image_path).convert("RGBA")

    # 生成Android icon
    round_icon = circle_corner(img_file, radii=24)
    circle_icon = circle_corner(img_file, radii=int(img_file.height / 2))
    foreground_icon = circle_corner(img_file, radii=0)
    for index, size in enumerate(androidIconSize):
        # 图片完整名称
        dpi_dir = img_dir + '/' + androidNames[index] + "/"
        if not os.path.exists(dpi_dir):
            os.makedirs(dpi_dir)
        # 前景色尺寸
        foreground_size = int(size * 2.25)
        # 圆角矩形
        round_im = round_icon.resize((size, size), Image.BILINEAR)
        round_name = dpi_dir + "ic_launcher.png"
        round_im.save(round_name, "png")
        # 圆形
        circle_im = circle_icon.resize((size, size), Image.BILINEAR)
        circle_name = dpi_dir + "ic_launcher_round.png"
        circle_im.save(circle_name, "png")
        # 前景色
        foreground_im = foreground_icon.resize((foreground_size, foreground_size), Image.BILINEAR)
        foreground_name = dpi_dir + "ic_launcher_foreground.png"
        foreground_im.save(foreground_name, "png")


create_android_icon(path)
