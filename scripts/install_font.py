#!/usr/bin/env python3
"""
字体安装辅助脚本
帮你把 LXGW WenKai npm 包的 woff2 子集合并为单个 TTF 文件

使用方法：
    python3 scripts/install_font.py
"""

import os
import sys
import shutil
import platform

def install_from_npm():
    """从 npm 安装字体包并合并子集"""
    print("📦 正在安装 lxgw-wenkai-webfont npm 包...")
    os.system("npm install lxgw-wenkai-webfont --prefix .")

    pkg_dir = os.path.join(os.getcwd(), "node_modules", "lxgw-wenkai-webfont", "files")
    if not os.path.exists(pkg_dir):
        print("❌ npm 包安装失败或目录不存在")
        return False

    # 合并所有 woff2
    print("🔧 正在合并字体子集（这可能需要几分钟）...")
    from fontTools.ttLib import TTFont
    import glob

    fonts = sorted(glob.glob(os.path.join(pkg_dir, "*.woff2")))
    if not fonts:
        print("❌ 未找到 woff2 文件")
        return False

    print(f"   找到 {len(fonts)} 个字体子集文件")

    # 加载第一个作为基础
    merged = TTFont(fonts[0])
    for f in fonts[1:]:
        font = TTFont(f)
        for tag in font.keys():
            if tag not in merged:
                merged[tag] = font[tag]

    # 保存到 /tmp/fonts/
    font_dir = "/tmp/fonts"
    os.makedirs(font_dir, exist_ok=True)
    out_path = os.path.join(font_dir, "LXGWWenKai-Merged.ttf")
    merged.save(out_path)

    print(f"✅ 字体已安装: {out_path}")
    print(f"   大小: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")

    # 清理 npm 包
    shutil.rmtree(os.path.join(os.getcwd(), "node_modules"))
    os.remove(os.path.join(os.getcwd(), "package.json"))
    os.remove(os.path.join(os.getcwd(), "package-lock.json"))

    return True


def install_from_github():
    """直接从 GitHub 下载 TTF"""
    import urllib.request
    import zipfile
    import io

    print("⬇️  正在从 GitHub 下载字体...")
    url = "https://github.com/lxgw/LxgwWenKai/releases/download/v1.501/LXGWWenKai_v1.501.zip"
    
    try:
        response = urllib.request.urlopen(url, timeout=30)
        data = response.read()
        z = zipfile.ZipFile(io.BytesIO(data))
        
        font_dir = "/tmp/fonts"
        os.makedirs(font_dir, exist_ok=True)
        
        for name in z.namelist():
            if name.endswith('.ttf') and 'Regular' in name:
                content = z.read(name)
                out_path = os.path.join(font_dir, "LXGWWenKai-Regular.ttf")
                with open(out_path, 'wb') as f:
                    f.write(content)
                print(f"✅ 字体已安装: {out_path}")
                return True
        print("❌ 压缩包中未找到 Regular TTF 文件")
        return False
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def main():
    system = platform.system()
    print(f"🖥️  检测到系统: {system}")
    print()

    # 检查是否已有字体
    existing = "/tmp/fonts/LXGWWenKai-Merged.ttf"
    if os.path.exists(existing):
        print(f"✅ 字体已存在: {existing}")
        return

    # 尝试自动安装
    print("正在安装霞鹜文楷字体...")
    print()
    
    if system == "Darwin":
        # macOS
        result = os.system("brew install font-lxgw-wenkai 2>/dev/null")
        if result == 0:
            print("✅ 通过 Homebrew 安装成功")
            # 复制到 /tmp/fonts/
            import glob
            paths = glob.glob(os.path.expanduser(
                "~/Library/Fonts/nguWenKai*.ttf"
            )) + glob.glob(os.path.expanduser(
                "~/Library/Fonts/LXGWWenKai*.ttf"
            ))
            if paths:
                os.makedirs("/tmp/fonts", exist_ok=True)
                shutil.copy(paths[0], "/tmp/fonts/LXGWWenKai-Merged.ttf")
                print(f"✅ 已复制到: /tmp/fonts/LXGWWenKai-Merged.ttf")
                return
        
        print("Homebrew 未找到，自动下载...")
        install_from_github()

    elif system == "Linux":
        result = os.system("which apt-get && sudo apt-get install -y fonts-lxgw-wenkai 2>/dev/null")
        if result == 0:
            print("✅ 通过 apt 安装成功")
        else:
            install_from_github()

    else:
        # Windows 或其他
        install_from_github()

    print()
    print("📝 安装完成后，运行以下命令验证：")
    print("   python3 scripts/generate_card.py '测试文字'")


if __name__ == "__main__":
    main()
