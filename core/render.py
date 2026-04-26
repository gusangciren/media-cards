#!/usr/bin/env python3
"""
共享渲染核心库
处理字体加载、文本绘制、配置读取等通用功能
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json

# ========== 字体路径配置 ==========
# 默认字体路径（支持通过环境变量覆盖）
FONT_DIR = os.environ.get(
    "CARD_FONT_DIR",
    "/tmp/fonts"
)
FONT_PATH = os.path.join(FONT_DIR, "LXGWWenKai-Merged.ttf")

# 备选字体列表（按优先级）
FONT_FALLBACKS = [
    # macOS 常见中文手写字体
    "/System/Library/Fonts/Supplemental/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    # Linux
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    # Windows 常用中文字体路径
    "C:\\Windows\\Fonts\\STKAITI.TTF",      # 华文楷体
    "C:\\Windows\\Fonts\\STSONG.TTF",        # 华文宋体
    "C:\\Windows\\Fonts\\simsun.ttc",        # 宋体
    "C:\\Windows\\Fonts\\msyh.ttc",          # 微软雅黑
    "C:\\Windows\\Fonts\\simkai.ttf",        # 楷体
    # 用户指定
    FONT_PATH,
]

def find_available_font(preferred=None):
    """查找第一个可用的中文字体"""
    candidates = ([preferred] if preferred else []) + FONT_FALLBACKS
    for path in candidates:
        if path and os.path.exists(path):
            try:
                ImageFont.truetype(path, 20)
                return path
            except Exception:
                pass
    # 最后尝试系统默认
    try:
        return ImageFont.truetype("Pillow/Tests/fonts/DejaVuSans.ttf", 20)
    except:
        return None

def get_font(size, path=None):
    """获取指定字号的字体对象"""
    font_path = path or FONT_PATH
    if not os.path.exists(font_path):
        font_path = find_available_font(font_path)
    if not font_path:
        raise FileNotFoundError(
            f"未找到可用字体。请确保霞鹜文楷(LXGWWenKai-Merged.ttf)已安装并设置到 "
            f"$CARD_FONT_DIR 或 /tmp/fonts/"
        )
    return ImageFont.truetype(font_path, size)

# ========== 文本工具 ==========

def wrap_text(text, font, max_width):
    """
    按字符换行，保持中文完整
    
    Args:
        text: 要换行的文本
        font: PIL ImageFont 对象
        max_width: 最大宽度（像素）
    
    Returns:
        list[str]: 换行后的行列表
    """
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue
        line = ''
        for char in paragraph:
            test = line + char
            bbox = font.getbbox(test)
            if bbox[2] - bbox[0] > max_width:
                if line:
                    lines.append(line)
                line = char
            else:
                line = test
        if line:
            lines.append(line)
    return lines


def draw_wrapped_text(draw, text, x, y, font, fill, max_width, line_spacing=1.6):
    """
    绘制自动换行的文本
    
    Args:
        draw: ImageDraw 对象
        text: 文本内容
        x, y: 起始坐标
        font: 字体
        fill: 颜色
        max_width: 最大宽度
        line_spacing: 行距倍数
    
    Returns:
        int: 绘制后的 y 坐标
    """
    lines = wrap_text(text, font, max_width)
    current_y = y
    for line in lines:
        if line == '':
            current_y += int(font.size * 0.6)
            continue
        draw.text((x, current_y), line, fill=fill, font=font)
        bbox = font.getbbox(line)
        line_h = bbox[3] - bbox[1]
        current_y += int(line_h * line_spacing)
    return current_y


def text_center(draw, text, y, font, fill, canvas_width=1080):
    """水平居中绘制单行文本"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    # 优先使用 getlength（PIL 10+），否则用 canvas_width 计算
    if hasattr(font, 'getlength'):
        tw = font.getlength(text)
    x = (canvas_width - tw) // 2
    draw.text((x, y), text, fill=fill, font=font)


def load_avatar(avatar_path, size=120):
    """
    加载头像并裁剪为正方形圆形
    
    Args:
        avatar_path: 头像图片路径
        size: 输出尺寸
    
    Returns:
        tuple: (带圆形遮罩的PIL Image, 原始尺寸)
    """
    if not os.path.exists(avatar_path):
        raise FileNotFoundError(f"头像文件不存在: {avatar_path}")
    
    avatar = Image.open(avatar_path).convert('RGB')
    w, h = avatar.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    avatar = avatar.crop((left, top, left + min_dim, top + min_dim))
    avatar = avatar.resize((size, size), Image.Resampling.LANCZOS)
    
    # 创建圆形遮罩
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, size, size], fill=255)
    avatar.putalpha(mask)
    
    return avatar


def hex_to_rgb(hex_color):
    """#RRGGBB 格式转 RGB 元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def load_config(skill_dir=None):
    """加载品牌配置文件"""
    if skill_dir is None:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(skill_dir, "config", "brand.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {}
