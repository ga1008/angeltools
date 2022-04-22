# -*- coding: utf-8 -*-
import io
import os
from pathlib import Path


def image2chars(image_path, width=120, k=1.0, reverse=False, outfile=None, chart_list=None):
    """
    照片转为字符，默认120个字符宽度
    """
    from PIL import Image
    import numpy as np

    im = Image.open(image_path).convert("L")  # 打开图片文件，转为灰度格式
    height = int(k * width * im.size[1] / im.size[0])  # 打印图像高度，k为矫正系数，用于矫正不同终端环境像素宽高比
    # im.show()
    arr = np.array(im.resize((width, height)))  # 转为NumPy数组
    if reverse:  # 反色处理
        arr = 255 - arr

    chart_list = chart_list if chart_list else [" ", ".", "-", "+", "=", "*", "#", "@"]   # 灰度-字符映射表
    chs = np.array(chart_list)
    arr = chs[(arr / (int(255/len(chart_list))+1)).astype(np.uint8)]  # 灰度转为对应字符

    if outfile:
        with open(outfile, "w") as fp:
            for row in arr.tolist():
                fp.write("".join(row))
                fp.write("\n")
    else:
        for i in range(arr.shape[0]):  # 逐像素打印
            for j in range(arr.shape[1]):
                print(arr[i, j], end=" ")
            print()


def text2image(text, size=None, font_color=None, back_color=None, save_path=None, font_path=None):
    """
    文字转照片
    :param text:
    :param size:
    :param font_color:
    :param back_color:
    :param save_path:
    :param font_path:
    :return:
    """
    import pygame

    font_path = font_path if font_path else pygame.font.get_default_font()
    size = int(size) if size else 50
    font_color = tuple(font_color) if font_color else (0, 0, 0)
    back_color = tuple(back_color) if back_color else (255, 255, 255)

    if save_path:
        save_path = Path(save_path)
        if save_path.exists():
            os.remove(save_path.absolute())
        save_path = str(save_path.absolute())
    else:
        save_path = io.BytesIO()

    pygame.init()
    font = pygame.font.Font(font_path, size)
    render_text = font.render(text, True, font_color, back_color)

    pygame.image.save(render_text, save_path)
    return save_path


def text2chars(text, font_path=None, width=None, k=None, outfile=None, chart_list=None):
    img = text2image(text, size=100, font_path=font_path)
    image2chars(img, width=width, k=k, outfile=outfile, reverse=True, chart_list=chart_list)


if __name__ == "__main__":
    text2image(
        'ABC',
        size=50,
        font_path='/etc/fonts/msyh.ttf',
        font_color=[0, 0, 0],
        back_color=[],
        save_path='/home/ABC.png'
    )

    # image2chars(
    #     '/home/测试123.png',
    #     width=100,
    #     k=0.6,
    #     # outfile='/home/测试123.txt',
    #     reverse=True
    # )

    # text2chars(
    #     "ANGEL",
    #     # font_path='/etc/fonts/msyh.ttf',
    #     width=50,
    #     k=0.6,
    #     # outfile='/home/测试123.txt',
    #     chart_list=[' ', '-', '/', '%'],
    # )
