#!/usr/bin/env python3
"""
小红书轮播卡生成器 — 砚石黑风格

使用方法：
    python3 carousel_template.py --title "标题" --subtitle "副标题" --cards '[{"title":"卡片标题","body":"卡片内容"}]'

或者：
    python3 carousel_template.py --interactive
"""

from PIL import Image, ImageDraw
import os
import sys
import json
import argparse

# 添加 core 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.render import get_font, wrap_text, draw_wrapped_text, load_config

# ========== 设计规格（可配置） ==========
DEFAULT_CONFIG = {
    "carousel": {
        "brand": "你的品牌",
        "accent_color": [197, 61, 67],
        "bg_color": [26, 26, 26],
        "text_primary": [240, 237, 232],
        "text_secondary": [138, 130, 120],
    }
}

def get_config():
    """加载配置，优先读文件，缺失则用默认值"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_cfg = load_config(skill_dir)
    cfg = DEFAULT_CONFIG.copy()
    if file_cfg:
        if "carousel" in file_cfg:
            cfg["carousel"].update(file_cfg["carousel"])
        if "card" in file_cfg:
            cfg["card"] = file_cfg["card"]
    return cfg


# ========== 画布常量 ==========
W, H = 1080, 1440
MARGIN = 80


def get_style(cfg):
    return {
        "BG": tuple(cfg["carousel"].get("bg_color", [26, 26, 26])),
        "ACCENT": tuple(cfg["carousel"].get("accent_color", [197, 61, 67])),
        "TEXT_PRIMARY": tuple(cfg["carousel"].get("text_primary", [240, 237, 232])),
        "TEXT_SECONDARY": tuple(cfg["carousel"].get("text_secondary", [138, 130, 120])),
        "BRAND": cfg["carousel"].get("brand", "你的品牌"),
    }


# ========== 绘图工具 ==========

def draw_seal(draw, x, y, size=60, fill=(197, 61, 67)):
    draw.ellipse([x, y, x+size, y+size], fill=fill)


def draw_line_h(draw, y, width=3, fill=(197, 61, 67)):
    """水平红线"""
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=fill, width=width)


def draw_line_centered(draw, y, line_w=160, width=3, fill=(197, 61, 67)):
    """居中水平红线"""
    x = (W - line_w) // 2
    draw.line([(x, y), (x + line_w, y)], fill=fill, width=width)


def text_left(draw, text, x, y, font, fill=(240, 237, 232)):
    draw.text((x, y), text, fill=fill, font=font)


def text_center(draw, text, y, font, fill=(240, 237, 232)):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, fill=fill, font=font)


# ========== 卡片函数 ==========

def card_cover(title, subtitle="", tagline="", cfg=None):
    """
    封面卡 — 标题居中放大版
    
    Args:
        title: 主标题（可含换行符）
        subtitle: 副标题
        tagline: 金句
        cfg: 配置字典
    
    Returns:
        输出路径
    """
    cfg = cfg or get_config()
    s = get_style(cfg)
    img = Image.new('RGB', (W, H), s["BG"])
    d = ImageDraw.Draw(img)

    # 顶部装饰线 + 右侧印章
    draw_line_h(d, 100, width=4)
    draw_seal(d, W - MARGIN - 50, 70, 50)

    # 标签（可自定义）
    text_left(d, "阅读方法论", MARGIN, 160, get_font(28), fill=s["ACCENT"])

    # ===== 标题区：居中放大 =====
    title_font = get_font(140)
    sub_font = get_font(68)

    max_title_w = W - 2 * MARGIN
    title_lines = wrap_text(title, title_font, max_title_w)
    title_line_h = int(140 * 1.2)

    total_title_h = len(title_lines) * title_line_h
    sub_h = 80
    sep_h = 60

    total_block_h = total_title_h + sep_h + sub_h
    available_top = 240
    available_bottom = 1200
    available_h = available_bottom - available_top
    block_y = available_top + (available_h - total_block_h) // 3

    # 绘制标题（居中）
    current_y = block_y
    for line in title_lines:
        text_center(d, line, current_y, title_font, fill=s["TEXT_PRIMARY"])
        current_y += title_line_h

    # 副标题
    if subtitle:
        current_y += sep_h
        text_center(d, subtitle, current_y, sub_font, fill=s["TEXT_PRIMARY"])
        current_y += sub_h

    # 红色分隔线（居中）
    draw_line_centered(d, current_y + 30, line_w=160)
    current_y += 70

    # 金句
    if tagline:
        text_center(d, tagline, current_y, get_font(34), fill=s["TEXT_SECONDARY"])

    # 底部大印章「读」
    draw_seal(d, W//2 - 55, 900, 110)
    text_center(d, "读", 918, get_font(52), fill=(255, 255, 255))

    # 底部品牌
    text_left(d, s["BRAND"], MARGIN, 1300, get_font(26), fill=s["TEXT_SECONDARY"])
    draw_line_h(d, 1360, width=2)

    output_dir = os.path.expanduser("~/.qclaw/workspace")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "xhs-01-cover.png")
    img.save(path, quality=95)
    print(f"封面: {path}")
    return path


def card_content(num, title, body, cfg=None):
    """
    内容卡 — 带编号和正文
    
    Args:
        num: 编号（1-99）
        title: 卡片标题
        body: 正文内容
        cfg: 配置字典
    
    Returns:
        输出路径
    """
    cfg = cfg or get_config()
    s = get_style(cfg)
    img = Image.new('RGB', (W, H), s["BG"])
    d = ImageDraw.Draw(img)

    # 顶部红线 + 编号
    draw_line_h(d, 100, width=3)
    text_left(d, f"{num:02d}", MARGIN, 140, get_font(90), fill=s["ACCENT"])

    # 标题
    text_left(d, title, MARGIN, 280, get_font(56), fill=s["TEXT_PRIMARY"])
    draw.line([(MARGIN, 360), (MARGIN + 180, 360)], fill=s["ACCENT"], width=3)

    # 正文
    draw_wrapped_text(
        d, body, MARGIN, 450,
        get_font(52), s["TEXT_PRIMARY"],
        W - 2 * MARGIN, line_spacing=1.9
    )

    # 右下角印章
    draw_seal(d, W - MARGIN - 70, 1200, 70)
    draw_line_h(d, 1360, width=2)

    output_dir = os.path.expanduser("~/.qclaw/workspace")
    os.makedirs(output_dir, exist_ok=True)
    slug = title[:4].replace("/", "").replace("\\", "")
    path = os.path.join(output_dir, f"xhs-{num+1:02d}-{slug}.png")
    img.save(path, quality=95)
    print(f"卡片{num:02d}: {path}")
    return path


def card_ending(quote="", cfg=None, keywords=None):
    """
    结尾卡 — 金句 + 品牌引导 + 标签
    
    Args:
        quote: 结尾金句
        cfg: 配置字典
        keywords: 话题标签列表
    
    Returns:
        输出路径
    """
    cfg = cfg or get_config()
    s = get_style(cfg)
    img = Image.new('RGB', (W, H), s["BG"])
    d = ImageDraw.Draw(img)

    draw_line_h(d, 100, width=3)

    # 金句
    y = 350
    for line in quote.split('\n'):
        if line.strip():
            # 突出「不」字所在行为红色
            fill = s["ACCENT"] if '不' in line else s["TEXT_PRIMARY"]
            text_center(d, line, y, get_font(48), fill=fill)
            y += 75

    # 大印章
    draw_seal(d, W//2 - 50, y + 20, 100)
    draw_line_h(d, 800, width=2)

    # 品牌引导（不使用"公众号"字眼）
    text_center(d, "更多内容", 870, get_font(32), fill=s["TEXT_SECONDARY"])
    text_center(d, f"「{s['BRAND']}」", 940, get_font(42), fill=s["TEXT_PRIMARY"])

    # 话题标签
    if keywords:
        kw_font = get_font(26)
        kw_y = 1040
        kw_x = MARGIN
        for kw in keywords:
            tag = f"#{kw}"
            bbox = kw_font.getbbox(tag)
            tw = bbox[2] - bbox[0]
            d.rounded_rectangle(
                [kw_x, kw_y, kw_x + tw + 20, kw_y + 40],
                radius=6, outline=s["ACCENT"], width=1
            )
            text_left(d, tag, kw_x + 10, kw_y + 6, kw_font, fill=s["ACCENT"])
            kw_x += tw + 40
            if kw_x > W - 200:
                kw_x = MARGIN
                kw_y += 55

    draw_line_h(d, 1360, width=2)

    output_dir = os.path.expanduser("~/.qclaw/workspace")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "xhs-07-ending.png")
    img.save(path, quality=95)
    print(f"结尾: {path}")
    return path


def generate_carousel(content, cfg=None):
    """
    生成完整轮播卡组
    
    Args:
        content: 包含以下字段的字典：
            - title: 主标题
            - subtitle: 副标题（可选）
            - tagline: 一句话金句（可选）
            - cards: [{title, body}, ...] 内容卡列表
            - ending_quote: 结尾金句
            - keywords: 话题标签列表
        cfg: 配置字典（可选）
    
    Returns:
        list[str]: 生成的图片路径列表
    """
    cfg = cfg or get_config()
    paths = []

    # 封面
    paths.append(card_cover(
        content.get("title", ""),
        content.get("subtitle", ""),
        content.get("tagline", ""),
        cfg=cfg
    ))

    # 内容卡（最多5张）
    for i, card in enumerate(content.get("cards", [])[:5], start=1):
        paths.append(card_content(i, card["title"], card["body"], cfg=cfg))

    # 结尾
    paths.append(card_ending(
        content.get("ending_quote", ""),
        cfg=cfg,
        keywords=content.get("keywords", [])
    ))

    return paths


# ========== 命令行入口 ==========

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="生成小红书轮播卡（砚石黑风格）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 carousel_template.py \\
    --title "卖掉副产品" \\
    --subtitle "为什么最聪明的商业头脑都在捡垃圾" \\
    --tagline "你扔掉的东西里，藏着下一个利润来源" \\
    --cards '[{"title":"副产品无处不在","body":"..."}]' \\
    --ending "发现别人忽视的价值，你就能发现别人看不见的利润。" \\
    --keywords "副业,商业思维,赚钱"

交互模式：
  python3 carousel_template.py --interactive
        """
    )
    parser.add_argument("--title", required=True, help="主标题")
    parser.add_argument("--subtitle", default="", help="副标题")
    parser.add_argument("--tagline", default="", help="一句话金句（封面用）")
    parser.add_argument("--cards", default="[]", help="卡片内容 JSON 数组")
    parser.add_argument("--ending", default="", help="结尾金句")
    parser.add_argument("--keywords", default="", help="话题标签，用逗号分隔")
    parser.add_argument("--output-dir", default=None, help="输出目录")
    parser.add_argument("--brand", default=None, help="品牌名（覆盖配置文件）")

    args = parser.parse_args()

    # 全局覆盖输出目录
    if args.output_dir:
        import core.render as r
        r._OUTPUT_DIR = os.path.expanduser(args.output_dir)

    # 全局覆盖品牌
    if args.brand:
        import core.render
        cfg = get_config()
        cfg["carousel"]["brand"] = args.brand
        local_cfg = cfg
    else:
        local_cfg = get_config()

    content = {
        "title": args.title,
        "subtitle": args.subtitle,
        "tagline": args.tagline,
        "cards": json.loads(args.cards),
        "ending_quote": args.ending,
        "keywords": [k.strip() for k in args.keywords.split(",") if k.strip()]
    }

    print("\n" + "="*50)
    print("生成轮播卡...")
    paths = generate_carousel(content, cfg=local_cfg)
    print("="*50)
    print(f"\n✅ 生成完成！共 {len(paths)} 张")
    for p in paths:
        print(f"  {p}")
