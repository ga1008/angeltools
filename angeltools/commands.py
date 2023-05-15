import argparse
import json
import os.path
from pathlib import Path


def txt2chars(args=None):
    dp = ' *** 文字转字符块小工具'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("text", type=str, default='Hello', help=f'{da} 任何文字')
    parser.add_argument("-f", "--font_path", type=str, dest="font_path",
                        default=None, help=f'{da} 指定字体文件，默认使用系统字体')
    parser.add_argument("-w", "--width", type=int, dest="width",
                        default=100, help=f'{da} 输出字符块的宽度')
    parser.add_argument("-k", "--aspect_ratio", type=float, dest="aspect_ratio",
                        default=1.0, help=f'{da} 输出字符块的宽高比')
    parser.add_argument("-s", "--outfile", type=str, dest="outfile",
                        default=None, help=f'{da} 输出字符块位置，默认在终端打印不保存')
    parser.add_argument("-c", "--chart_list", type=str, dest="chart_list",
                        default='[" ", ".", "-", "+", "=", "*", "#", "@"]',
                        help=f'{da} 灰度字符列表，json格式，默认：[" ", ".", "-", "+", "=", "*", "#", "@"]')

    args = parser.parse_args()
    text = args.text
    font_path = args.font_path
    width = args.width
    aspect_ratio = args.aspect_ratio
    outfile = args.outfile
    chart_list = args.chart_list

    if not text and not text.strip():
        raise ValueError('空白文字')
    if font_path and not os.path.exists(font_path):
        raise ValueError(f"字体文件不存在: {font_path}")
    if width:
        try:
            width = int(width)
        except:
            raise ValueError('-w width 参数应该为int类型')
        if width <= 0:
            raise ValueError("-w width 参数应该大于0")
    if aspect_ratio:
        try:
            aspect_ratio = float(aspect_ratio)
        except:
            raise ValueError('-k aspect_ratio 参数应该为float类型')
        if aspect_ratio <= 0:
            raise ValueError("-k aspect_ratio 参数应该大于0")
    if outfile:
        outfile_path = Path(outfile)
        try:
            outfile_path.touch()
        except:
            raise ValueError(f'无法在此路径创建文件: {outfile_path.parent.absolute()}')
    if chart_list:
        try:
            chart_list = json.loads(chart_list)
        except:
            raise ValueError("-c chart_list 参数不正确")
    from angeltools.ImageTool import text2chars

    text2chars(
        text,
        font_path=font_path,
        width=width,
        k=aspect_ratio,
        outfile=outfile,
        chart_list=chart_list,
    )


def img2chars(args=None):
    dp = ' *** 图片转字符块小工具'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("image", type=str, default=None, help=f'{da} 图片路径')

    parser.add_argument("-w", "--width", type=int, dest="width",
                        default=100, help=f'{da} 输出字符块的宽度')
    parser.add_argument("-k", "--aspect_ratio", type=float, dest="aspect_ratio",
                        default=1.0, help=f'{da} 输出字符块的宽高比')
    parser.add_argument("-s", "--outfile", type=str, dest="outfile",
                        default=None, help=f'{da} 输出字符块位置，默认在终端打印不保存')
    parser.add_argument("-nr", "--not_reverse", type=bool, dest="not_reverse", nargs='?', default=False,
                        help=f'{da} 是否不先反转颜色再生成')
    parser.add_argument("-c", "--chart_list", type=str, dest="chart_list",
                        default='[" ", ".", "-", "+", "=", "*", "#", "@"]',
                        help=f'{da} 灰度字符列表，json格式，默认：[" ", ".", "-", "+", "=", "*", "#", "@"]')

    args = parser.parse_args()
    image = args.image
    width = args.width
    aspect_ratio = args.aspect_ratio
    outfile = args.outfile
    reverse = True if not args.not_reverse else False
    chart_list = args.chart_list

    if not image and not image.strip():
        raise ValueError('空白图片路径')

    if width:
        try:
            width = int(width)
        except:
            raise ValueError('-w width 参数应该为int类型')
        if width <= 0:
            raise ValueError("-w width 参数应该大于0")
    if aspect_ratio:
        try:
            aspect_ratio = float(aspect_ratio)
        except:
            raise ValueError('-k aspect_ratio 参数应该为float类型')
        if aspect_ratio <= 0:
            raise ValueError("-k aspect_ratio 参数应该大于0")
    if outfile:
        outfile_path = Path(outfile)
        try:
            outfile_path.touch()
        except:
            raise ValueError(f'无法在此路径创建文件: {outfile_path.parent.absolute()}')
    if chart_list:
        try:
            chart_list = json.loads(chart_list)
        except:
            raise ValueError("-c chart_list 参数不正确")
    from angeltools.ImageTool import image2chars

    image2chars(
        image_path=image,
        width=width,
        k=aspect_ratio,
        outfile=outfile,
        reverse=reverse,
        chart_list=chart_list
    )


def text_sorted_by_first_pinyin(args=None):
    dp = ' *** a tool to sorted text lines by first pinyin letter'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("file_path", type=str, default=None, help=f'{da} 路径')

    parser.add_argument("-p", "--save_path", type=str, dest="save_path",
                        default=None, help=f'{da} save 路径')

    parser.add_argument("-f", "--full_match", type=bool, dest="full_match", nargs='?', default=False,
                        help=f'{da} match all pinyin letters')

    parser.add_argument("-r", "--reverse", type=bool, dest="reverse", nargs='?', default=False,
                        help=f'{da} 反转')

    from angeltools.StrTool import SortedWithFirstPinyin

    args = parser.parse_args()

    file_path = args.file_path
    save_path = args.save_path
    reverse = True if args.reverse else False
    full_match = True if args.full_match else False
    SortedWithFirstPinyin(
        file_path=file_path,
        save_path=save_path,
        full_match=full_match,
        reverse=reverse,
    ).run()


if __name__ == '__main__':
    txt2chars()
