# 📚 media-cards — 自媒体卡片生成器

一键将**长篇文章**拆成小红书轮播图，或把**短金句**做成精美的知识卡。

> 本项目源于 QClaw/OpenClaw 个人助理的技能，已开源供所有人使用。

---

## ✨ 两种模式

| 模式 | 输入 | 输出 | 尺寸 | 风格 |
|------|------|------|------|------|
| **轮播卡** | 长文章（200字+） | 封面 + N张内容 + 结尾 | 1080 × 1440 | 砚石黑 + 朱砂红 |
| **知识卡** | 短金句（<200字） | 单张卡片 | 1179 × 1572 | 白底 + 红边框 |

---

## 🚀 快速开始

### 第一步：安装字体

本工具使用**霞鹜文楷**字体实现中文手写效果。

```bash
# macOS
brew install font-lxgw-wenkai

# Linux（Debian/Ubuntu）
sudo apt install fonts-lxgw-wenkai

# 通用：运行字体安装脚本
python3 scripts/install_font.py
```

### 第二步：安装依赖

```bash
pip3 install Pillow fonttools brotli
```

### 第三步：克隆并使用

```bash
git clone https://github.com/你的用户名/media-cards.git
cd media-cards

# 试试轮播卡
python3 scripts/carousel_template.py \
  --title "卖掉副产品" \
  --cards '[{"title":"副产品无处不在","body":"当你生产某样东西时，总会同时产出其他东西。木材商把树砍成木板，剩下的锯末和边角料就成了副产品。"}]'

# 试试知识卡
python3 scripts/generate_card.py "相信你的读者，他们比你想象的更聪明。"
```

---

## 📖 使用详解

### 轮播卡 — 将长文章变成小红书轮播

适合将公众号文章、博客长文拆成 6-8 张图文卡片。

```bash
python3 scripts/carousel_template.py \
  --title "卖掉副产品" \
  --subtitle "为什么最聪明的商业头脑都在捡垃圾" \
  --tagline "你扔掉的东西里，藏着下一个利润来源" \
  --cards '[
    {"title":"副产品无处不在","body":"当你生产某样东西时，总会同时产出其他东西。木材商把树砍成木板，剩下的锯末和边角料就成了锯末、木片、燃料。这些「副产品」往往被当成垃圾处理，但你有没有想过——也许垃圾本身就是产品？"},
    {"title":"你的短视","body":"大多数企业只盯着自己生产的主要产品，从未认真审视过那些「废物」里藏着什么。结果呢？别人低价收购这些边角料，加工后卖出了高价，而你还在为如何处理它们发愁。"},
    {"title":"书籍作为副产品","body":"37signals 曾是一家网页设计公司。创始人在工作中积累了大量经验和见解，本打算写一本书来整理思路。结果书写完后，他们发现：这本书反而成了比设计服务更值钱的副产品。"},
    {"title":"意想不到的副产品","body":"亚马逊最初是一家在线书店，Jeff Bezos 很快意识到物流系统本身才是最有价值的副产品。如今，AWS 云服务每年带来数百亿美元收入，而它最初只是亚马逊的内部基础设施。"},
    {"title":"发现的艺术","body":"核心原则只有一个：当你生产任何东西时，问自己一个问题——这个东西的「废料」还能变成什么别人的产品？答案往往就是下一个利润来源。"}
  ]' \
  --ending "发现别人忽视的价值，你就能发现别人看不见的利润。" \
  --keywords "副业,商业思维,赚钱"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--title` | ✅ | 主标题（封面大标题） |
| `--subtitle` | | 副标题 |
| `--tagline` | | 一句话金句（封面用） |
| `--cards` | ✅ | JSON 数组，每张内容卡一条 |
| `--ending` | | 结尾金句 |
| `--keywords` | | 话题标签，逗号分隔 |
| `--brand` | | 品牌名（覆盖配置文件） |

### 知识卡 — 单条金句/洞见

适合单条洞见、语录、引用传播。原文原封不动呈现。

```bash
python3 scripts/generate_card.py "一旦培养出用户群体，你就不用再花钱去赚取眼球——人们会主动关注你。"
```

**⚠️ 核心规则：原文原封不动复制，不做任何编辑、提炼或改写。**

---

## ⚙️ 自定义配置

所有品牌信息集中在 `config/brand.json`，修改后立即生效：

```json
{
  "name": "你的名字",
  "handle": "@你的账号名",
  "avatar": "assets/avatar.jpg",
  "card": {
    "border_color": "#E53935",
    "border_width": 25,
    "canvas_width": 1179,
    "canvas_height": 1572,
    "font_size_body": 58
  },
  "carousel": {
    "brand": "你的品牌名",
    "accent_color": [197, 61, 67],
    "bg_color": [26, 26, 26]
  }
}
```

**关键配置项：**

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `card.border_color` | 知识卡边框颜色 | #E53935（红色） |
| `card.border_width` | 边框宽度（px） | 25 |
| `carousel.brand` | 轮播卡底部署名 | — |
| `carousel.accent_color` | 强调色 RGB | [197, 61, 67] 朱砂红 |
| `carousel.bg_color` | 轮播卡背景色 RGB | [26, 26, 26] 砚石黑 |

**头像**：将你的头像图片放到 `assets/avatar.jpg`（推荐 300×300 以上尺寸）

---

## 🎨 设计风格

### 轮播卡 — 砚石黑

```
┌─────────────────────────┐
│  ──────────  ●          │  顶部装饰线 + 印章
│  阅读方法论               │  标签
│                           │
│     【 主标题居中 】       │  140pt 加粗
│     【 副标题居中 】       │  68pt
│        ────              │  红色分隔线
│     「 金句 」            │  34pt
│                           │
│         读                │  底部大印章
│                           │
│  品牌名                    │  署名
└─────────────────────────┘

内容卡：
│  ────────────           │
│  01                     │  90pt 朱砂红编号
│  卡片标题                 │  56pt
│  ────                   │
│                          │
│  正文内容，自动换行        │  52pt
│  保留完整论证结构          │
│                     ●    │  右下印章
└─────────────────────────┘
```

### 知识卡 — 白底红框

```
│┌─────────────────────────┐│
││ [头像]  名字  ✓         ││  ← 三层认证徽章
││           @账号名        ││
││                          ││
││ 原文原封不动呈现          ││  ← 不做任何改写
││ 完整保留每个字和标点      ││
││                          ││
└└─────────────────────────┘│
        25px 红色边框
```

---

## 📁 目录结构

```
media-cards/
├── README.md               # 本文档
├── LICENSE                 # MIT 开源协议
├── .gitignore
├── config/
│   └── brand.json          # 品牌配置（修改这里）
├── core/
│   └── render.py           # 共享渲染库
├── scripts/
│   ├── carousel_template.py   # 轮播卡生成器
│   ├── generate_card.py        # 知识卡生成器
│   └── install_font.py         # 字体安装脚本
└── assets/
    └── avatar.jpg             # 头像（你自己放）
```

---

## 🧩 作为 QClaw/OpenClaw Skill 使用

如果你使用 QClaw 或 OpenClaw 个人助理，可以将本项目作为 Skill 安装：

```bash
# 复制到 skills 目录
cp -r media-cards ~/.openclaw/workspace/skills/

# 或者使用 skillhub
skillhub install media-cards
```

---

## ❓ 常见问题

**Q: 字体找不到？**

```bash
# macOS 确认字体已安装
ls ~/Library/Fonts/ | grep -i lxgw

# 设置字体路径
export CARD_FONT_DIR=~/Library/Fonts
```

**Q: Pillow 安装失败？**
```bash
pip3 install --upgrade pip
pip3 install Pillow
```

**Q: 轮播卡固定几张？**
不固定。根据内容长度自然拆分——内容多就多张，少就少张。核心结构保持：封面 + 内容卡 + 结尾。

**Q: 微信发图被压缩？**
图片保存为 PNG 格式，微信不会二次压缩。如需 JPG，在 `img.save()` 时改为 `quality=95, format='JPEG'`。

---

## 🤝 开源协议

**MIT License** — 随意修改、免费使用、商业也可。

如果你基于此项目做了有意思的改编，欢迎提 Issue 或 PR。
