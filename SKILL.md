---
name: media-cards
description: 自媒体卡片生成器 — 一键生成小红书轮播卡和知识卡。触发词：「自媒体卡片」。首次安装后运行 setup.py 完成配置。
---

# 自媒体卡片生成器 🎨

一键生成小红书/抖音风格的精美卡片，支持轮播图和单张知识卡两种格式。

---

## 🚀 首次安装

安装后，第一件事是配置你的品牌信息：

```bash
cd ~/.qclaw/skills/media-cards
python3 setup.py --name "你的名字" --handle "@你的账号" --avatar /path/to/avatar.jpg
```

**参数说明：**
| 参数 | 必填 | 说明 |
|------|------|------|
| `--name` | ✅ | 显示在卡片上的名字 |
| `--handle` | ✅ | 账号名（带 @，如 @像企业家一样写作） |
| `--avatar` | ❌ | 头像图片路径（也可之后手动放到 `assets/avatar.jpg`） |

**交互式配置**（不记得参数直接跑这个）：
```bash
python3 setup.py --interactive
```

---

## 📖 如何使用

**触发词：** `自媒体卡片`

把你想做成卡片的内容发给 OpenClaw，然后说「自媒体卡片」即可。

**自动判断内容类型：**

| 内容类型 | 判断规则 | 生成效果 | 示例 |
|---------|---------|---------|------|
| **长文** | 超过 200 字 | 7 张轮播卡（砚石黑风格） | 公众号文章拆解 |
| **金句** | 200 字以内 | 1 张知识卡（白底红框） | 一句话洞见 |

> OpenClaw 会自动判断，不需要你指定格式。

---

## 💡 使用示例

**示例 1：长文 → 轮播卡**
> 你：自媒体卡片
> [粘贴一篇公众号文章]
>
> → 自动拆解为 7 张小红书轮播图

**示例 2：金句 → 知识卡**
> 你：自媒体卡片
> Trust is not words, it is what you are willing to risk.
>
> → 自动生成一张白底知识卡

**示例 3：轮播卡封面优化**
> 用户反馈封面标题太小、躲在角落
> → 封面标题现在居中放大，占据主视觉区

---

## 🎨 输出说明

**轮播卡（长文）：**
- 尺寸：1080 × 1440（3:4，小红书最佳比例）
- 风格：砚石黑（深灰背景 #1A1A1A + 朱砂红强调）
- 结构：封面 + 5 张内容卡 + 结尾卡
- 字体：霞鹜文楷（自动安装，已内置于 skill）

**知识卡（金句）：**
- 尺寸：1179 × 1572（竖屏 3:4）
- 风格：白底红框（#E53935）+ 珊瑚橙强调
- 字体：霞鹜文楷

---

## ⚙️ 自定义配置

编辑 `config/brand.json` 来自定义：

```json
{
  "name": "你的名字",
  "handle": "@你的账号名",
  "avatar": "assets/avatar.jpg",
  "carousel": {
    "brand": "你的品牌名"
  }
}
```

---

## 🔧 故障排除

**字体显示异常（豆腐块）：**
```bash
# Mac：双击 fonts/LXGWWenKai-Merged.ttf，点"安装字体"
# Windows：将 fonts/LXGWWenKai-Merged.ttf 复制到 C:\Windows\Fonts\
```

**想更换头像：**
将新图片放到 `assets/avatar.jpg`，覆盖原文件。

---

## 📁 文件结构

```
media-cards/
├── SKILL.md           ← 你在这里
├── setup.py           ← 首次配置脚本
├── fonts/
│   └── LXGWWenKai-Merged.ttf  ← 内置字体
├── assets/
│   └── avatar.jpg     ← 你的头像
├── config/
│   └── brand.json     ← 品牌配置（setup.py 自动生成）
├── core/
│   └── render.py      ← 渲染核心
└── scripts/
    └── carousel_template.py  ← 轮播卡生成
```