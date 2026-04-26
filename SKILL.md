# 自媒体卡片 Skill

生成小红书风格轮播卡（砚石黑风格）。

## 触发词

**自媒体卡片**

用户发一段内容，说「自媒体卡片」后 AI 自动判断：
- 内容 <= 200字 -> 1张知识卡（白底红框）
- 内容 > 200字 -> 轮播卡（封面 + 内容 + 结尾，数量根据内容灵活决定）

## 轮播卡规范

**尺寸**：1080 x 1440（3:4竖屏，小红书最佳尺寸）

**数量**：根据内容长度和结构灵活决定，始终保持：
- 1张封面（无编号）
- N张内容卡（编号 01/02/...）
- 1张结尾卡（无编号）

不固定7张 -- 内容少则3-4张，内容多则8-10张，以内容完整呈现为准。

**风格**：砚石黑
- 背景：#0F0F0F
- 主色：珊瑚橙 #F55000
- 辅助：深灰 #333333 / 浅灰 #666666
- 文字：白色 #FFFFFF / 浅灰 #CCCCCC

**字体**：霞鹜文楷（内置于 skill，无需额外安装）

**布局**：
- 封面：品牌标题居中，无编号
- 内容卡：编号 + 标题 + 正文
- 结尾卡：无编号，含总结金句 + CTA

**字号层级**（参考值）：
- 编号：90pt
- 标题：56pt
- 正文：52pt
- 行距：1.9

## 安装

```bash
git clone https://github.com/gusangciren/media-cards ~/.qclaw/skills/media-cards
cd ~/.qclaw/skills/media-cards
python3 setup.py --name "你的名字" --handle "@你的账号" --avatar /path/to/avatar.jpg
```

## 首次配置

运行 `python3 setup.py` 配置品牌信息，生成 `config/brand.json`。

## 本地测试

```bash
cd ~/.qclaw/skills/media-cards
python3 scripts/carousel_template.py --content "你的内容"
```

## 目录结构

```
media-cards/
├── SKILL.md
├── setup.py
├── fonts/
│   └── LXGWWenKai-Merged.ttf  # 内置霞鹜文楷
├── config/
│   └── brand.json
├── assets/
│   └── avatar.jpg
├── core/
│   └── render.py
└── scripts/
    ├── carousel_template.py
    └── text_utils.py
```

## 故障排除

**字体不显示？**
```bash
python3 scripts/carousel_template.py --debug
```

**图片模糊？**
确保 avatar.jpg 分辨率 >= 300x300，格式为 JPG/PNG。
