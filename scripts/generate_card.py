#!/usr/bin/env python3
"""
小红书知识卡片生成脚本
核心规则：原文原封不动复制，不做任何编辑、提炼或改写
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import json
from datetime import datetime

# 添加 core 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.render import get_font, wrap_text, load_config, load_avatar, hex_to_rgb

# ========== 加载配置 ==========

def get_card_config():
    """加载品牌配置，优先读文件"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_cfg = load_config(skill_dir)
    
    defaults = {
        "name": "你的名字",
        "handle": "@你的账号名",
        "avatar": "assets/avatar.jpg",
        "card": {
            "canvas_width": 1179,
            "canvas_height": 1572,
            "border_color": "#E53935",
            "border_width": 25,
            "font_size_name": 56,
            "font_size_handle": 32,
            "font_size_body": 58,
            "content_y": 520,
            "line_height": 115,
            "avatar_size": 120,
            "avatar_x": 90,
            "avatar_y": 180,
        }
    }
    
    cfg = defaults.copy()
    cfg.update({k: v for k, v in file_cfg.items() if k in defaults})
    if "card" in file_cfg:
        cfg["card"].update(file_cfg["card"])
    
    return cfg


def get_font_for_card(size, skill_dir=None):
    """获取字体（带 fallback）"""
    import core.render
    try:
        return get_font(size)
    except FileNotFoundError:
        return ImageFont.truetype(
            "/System/Library/Fonts/PingFang.ttc", size
        )


def generate_card(user_text: str, output_path: str = None) -> str:
    """
    生成小红书知识卡片
    
    核心规则：原文原封不动复制，不做任何编辑、提炼或改写
    """
    cfg = get_card_config()
    card = cfg["card"]
    
    W = card["canvas_width"]
    H = card["canvas_height"]
    BORDER_C = hex_to_rgb(card["border_color"])
    BORDER_W = card["border_width"]

    # 创建画布（红色边框 + 白色内区）
    img = Image.new('RGB', (W, H), BORDER_C)
    draw = ImageDraw.Draw(img)
    inner = [BORDER_W, BORDER_W, W - BORDER_W, H - BORDER_W]
    draw.rectangle(inner, fill=(255, 255, 255))

    # 字体
    font_name = get_font_for_card(card["font_size_name"])
    font_handle = get_font_for_card(card["font_size_handle"])
    font_body = get_font_for_card(card["font_size_body"])

    # === 头像 ===
    avatar_rel = card["avatar"]
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    avatar_path = avatar_rel if os.path.isabs(avatar_rel) else os.path.join(skill_dir, avatar_rel)
    avatar_size = card["avatar_size"]
    avatar_x = card["avatar_x"]
    avatar_y = card["avatar_y"]

    if os.path.exists(avatar_path):
        try:
            avatar = load_avatar(avatar_path, avatar_size)
            img.paste(avatar, (avatar_x, avatar_y), avatar)
        except Exception as e:
            print(f"警告：头像加载失败 ({e})，跳过头像")
    else:
        print(f"警告：头像文件不存在: {avatar_path}")

    # === 头部文字 ===
    name_x = avatar_x + avatar_size + 30
    name_y = avatar_y + 10
    draw.text((name_x, name_y), cfg["name"], fill=(26, 26, 26), font=font_name)

    handle_y = name_y + 70
    draw.text((name_x, handle_y), cfg["handle"], fill=(102, 102, 102), font=font_handle)

    # 认证徽章：紧跟账号文字
    handle_bbox = draw.textbbox((name_x, handle_y), cfg["handle"], font=font_handle)
    badge_cx = handle_bbox[2] + 16
    badge_mid_y = (handle_y + handle_bbox[3]) / 2
    badge_r = 14

    # 三层：白环 + 深蓝底 + 白勾
    draw.ellipse(
        [badge_cx - badge_r - 2, badge_mid_y - badge_r - 2,
         badge_cx + badge_r + 2, badge_mid_y + badge_r + 2],
        fill=(255, 255, 255)
    )
    draw.ellipse(
        [badge_cx - badge_r, badge_mid_y - badge_r,
         badge_cx + badge_r, badge_mid_y + badge_r],
        fill=(26, 86, 219)  # #1A56DB
    )
    draw.line(
        [(badge_cx - 6, badge_mid_y), (badge_cx - 1, badge_mid_y + 5),
         (badge_cx + 7, badge_mid_y - 5)],
        fill=(255, 255, 255), width=3
    )

    # === 正文区域（原文原封不动）===
    margin = 100
    content_y = card["content_y"]
    line_h = card["line_height"]
    max_width = W - margin * 2

    lines = []
    for para in user_text.split('\n'):
        if not para:
            lines.append('')
            continue
        line = ''
        for char in para:
            test = line + char
            bbox = font_body.getbbox(test)
            if bbox[2] - bbox[0] > max_width:
                if line:
                    lines.append(line)
                line = char
            else:
                line = test
        if line:
            lines.append(line)

    for i, line in enumerate(lines):
        draw.text((margin, content_y + i * line_h), line,
                  fill=(26, 26, 26), font=font_body)

    # === 保存 ===
    if output_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/gusangciren_cards/card_{ts}.png"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")

    # 同时复制到 workspace
    workspace = os.path.expanduser("~/.qclaw/workspace/")
    if os.path.exists(workspace):
        import shutil
        shutil.copy(output_path, workspace)

    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_card.py <原文内容>")
        print("示例: python generate_card.py '相信你的读者'")
        sys.exit(1)

    user_text = sys.argv[1]
    output = generate_card(user_text)
    if output:
        print(f"✅ 卡片已生成: {output}")
