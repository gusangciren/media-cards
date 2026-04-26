#!/usr/bin/env python3
"""
媒体卡片生成器 — 核心渲染库

支持跨平台字体自动检测：优先使用 skill 内置字体，其次用户配置，最后系统字体
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys, json

# ========== 字体路径配置（按优先级） ==========

def _get_skill_dir():
    """获取 skill 目录（兼容直接运行和 import 两种方式）"""
    # 从本文件向上两级找到 skill 根目录
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUNDLED_FONT_DIR = os.path.join(_get_skill_dir(), "fonts")
BUNDLED_FONT = os.path.join(BUNDLED_FONT_DIR, "LXGWWenKai-Merged.ttf")

def find_font():
    """
    跨平台字体查找，按优先级：
    1. skill 内置字体（./fonts/LXGWWenKai-Merged.ttf）
    2. 用户配置目录 $CARD_FONT_DIR
    3. ~/.qclaw/fonts/
    4. 系统字体
    """
    candidates = [
        BUNDLED_FONT,
        os.environ.get("CARD_FONT_DIR"),
        os.path.expanduser("~/.qclaw/fonts/LXGWWenKai-Merged.ttf"),
        # macOS
        "/System/Library/Fonts/Supplemental/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        # Linux
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        # Windows
        "C:\\Windows\\Fonts\\STKAITI.TTF",
        "C:\\Windows\\Fonts\\STSONG.TTF",
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\simkai.ttf",
        "C:\\Windows\\Fonts\\simsun.ttc",
    ]
    for path in candidates:
        if path and os.path.exists(path):
            try:
                ImageFont.truetype(path, 20)
                return path
            except Exception:
                pass
    # 最后尝试系统默认（Windows 无字体时降级）
    try:
        return ImageFont.truetype("arial.ttf", 20)
    except:
        return None

def get_font(size, path=None):
    """获取指定字号的字体对象"""
    font_path = path or find_font()
    if not font_path:
        raise FileNotFoundError(
            "未找到可用中文字体。\n"
            "请确保已安装霞鹜文楷字体：\n"
            "  - Mac: 双击 fonts/LXGWWenKai-Merged.ttf → 点击\"安装字体\"\n"
            "  - Windows: 将 fonts/LXGWWenKai-Merged.ttf 复制到 C:\\Windows\\Fonts\\\n"
            "  - Linux: cp fonts/LXGWWenKai-Merged.ttf ~/.fonts/"
        )
    return ImageFont.truetype(font_path, size)

# ========== 文本工具 ==========

def wrap_text(text, font, max_width):
    """按字符换行，保持中文完整"""
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue
        line = ''
        for char in paragraph:
            test = line + char
            if hasattr(font, 'getlength'):
                tw = font.getlength(test)
            else:
                bbox = font.getbbox(test)
                tw = bbox[2] - bbox[0]
            if tw > max_width:
                if line:
                    lines.append(line)
                line = char
            else:
                line = test
        if line:
            lines.append(line)
    return lines

def draw_wrapped_text(draw, text, x, y, font, fill, max_width, line_spacing=1.6):
    """绘制自动换行的文本"""
    lines = wrap_text(text, font, max_width)
    current_y = y
    for line in lines:
        if line == '':
            current_y += int(font.size * 0.6)
            continue
        draw.text((x, current_y), line, fill=fill, font=font)
        if hasattr(font, 'getlength'):
            line_h = font.getlength("x") * line_spacing
        else:
            bbox = font.getbbox(line)
            line_h = (bbox[3] - bbox[1]) * line_spacing
        current_y += int(line_h)
    return current_y

def text_center(draw, text, y, font, fill, canvas_width=1080):
    """水平居中绘制单行文本"""
    if hasattr(font, 'getlength'):
        tw = font.getlength(text)
    else:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
    x = (canvas_width - tw) // 2
    draw.text((x, y), text, fill=fill, font=font)

# ========== 头像加载 ==========

def load_avatar(avatar_path, size=120):
    """加载头像并裁剪为正方形圆形"""
    if not os.path.exists(avatar_path):
        raise FileNotFoundError(f"头像文件不存在: {avatar_path}")
    avatar = Image.open(avatar_path).convert('RGB')
    w, h = avatar.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    avatar = avatar.crop((left, top, left + min_dim, top + min_dim))
    avatar = avatar.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, size, size], fill=255)
    avatar.putalpha(mask)
    return avatar

# ========== 配置工具 ==========

def hex_to_rgb(hex_color):
    """#RRGGBB 格式转 RGB 元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def load_config(skill_dir=None):
    """加载品牌配置文件"""
    if skill_dir is None:
        skill_dir = _get_skill_dir()
    cfg_path = os.path.join(skill_dir, "config", "brand.json")
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            return json.load(f)
    return {}

def save_config(cfg, skill_dir=None):
    """保存品牌配置文件"""
    if skill_dir is None:
        skill_dir = _get_skill_dir()
    cfg_path = os.path.join(skill_dir, "config", "brand.json")
    with open(cfg_path, "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)