#!/usr/bin/env python3
"""
首次配置向导 — 媒体卡片 skill

运行方式：
    python3 setup.py --name "你的名字" --handle "@你的账号" --avatar /path/to/avatar.jpg

或交互模式：
    python3 setup.py --interactive
"""
import os, sys, json, shutil, argparse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config", "brand.json")
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")
TEMPLATE_CONFIG = {
    "name": "你的名字",
    "handle": "@你的账号名",
    "avatar": "assets/avatar.jpg",
    "card": {
        "border_color": "#E53935",
        "border_width": 25,
        "canvas_width": 1179,
        "canvas_height": 1572,
        "font_size_name": 56,
        "font_size_handle": 32,
        "font_size_body": 58,
        "content_y": 520,
        "line_height": 115
    },
    "carousel": {
        "brand": "你的品牌",
        "accent_color": [197, 61, 67],
        "font_size_tag": 28,
        "font_size_title": 140,
        "font_size_subtitle": 68,
        "font_size_tagline": 34,
        "font_size_num": 90,
        "font_size_content_title": 56,
        "font_size_content_body": 52,
        "font_size_quote": 48,
        "font_size_author": 26,
        "font_size_ending": 42
    }
}

def interactive_setup():
    print("\n📝 媒体卡片 skill 首次配置\n" + "="*40)
    name = input("你的名字（显示在卡片上）: ").strip()
    handle = input("账号名（格式 @xxx）: ").strip()
    if not handle.startswith("@"):
        handle = "@" + handle
    
    avatar_path = input("头像图片路径（直接回车跳过，之后手动放到 assets/avatar.jpg）: ").strip()
    return name, handle, avatar_path

def run_setup(name, handle, avatar_path=None, interactive=False):
    if interactive and not name:
        name, handle, avatar_path = interactive_setup()
    
    if not name or not handle:
        print("❌ 错误：名字和账号名必填")
        print("   用法: python3 setup.py --name \"张三\" --handle \"@zhangsan\" --avatar /path/to/avatar.jpg")
        return False
    
    cfg = TEMPLATE_CONFIG.copy()
    cfg["name"] = name
    cfg["handle"] = handle
    
    # 如果提供了头像，复制到 assets/
    if avatar_path and os.path.exists(os.path.expanduser(avatar_path)):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        src = os.path.expanduser(avatar_path)
        dst = os.path.join(ASSETS_DIR, "avatar.jpg")
        shutil.copy2(src, dst)
        cfg["avatar"] = "assets/avatar.jpg"
        print(f"✅ 头像已复制到 {dst}")
    
    # 保存配置
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置已保存！")
    print(f"   名字: {name}")
    print(f"   账号: {handle}")
    print(f"\n🚀 配置完成！现在可以对 OpenClaw 说「自媒体卡片」使用了。")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="媒体卡片 skill 首次配置")
    parser.add_argument("--name", default="", help="你的名字")
    parser.add_argument("--handle", default="", help="账号名（如 @xxx）")
    parser.add_argument("--avatar", default="", help="头像图片路径")
    parser.add_argument("--interactive", action="store_true", help="交互式配置")
    args = parser.parse_args()
    
    run_setup(
        name=args.name or "",
        handle=args.handle or "",
        avatar_path=args.avatar or "",
        interactive=args.interactive
    )