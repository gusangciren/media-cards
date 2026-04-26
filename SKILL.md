---
name: media-cards
description: 自媒体内容卡片一键生成。当用户说"自媒体卡片"、给一篇文章要求拆卡、或发送单句/金句做卡片时触发。核心判断：文章内容（超过200字或多个段落）走Python轮播脚本（数量根据内容灵活决定）；单句或金句（200字以内且单段落）走xhs-knowledge-card技能（单张白底知识卡）。
---

# 自媒体卡片生成

## 铁律：数量不固定

**轮播卡数量永远不固定。** 根据内容长度自然决定张数，保持：
- 1张封面（无编号）
- N张内容卡（编号 01, 02, ...）
- 1张结尾卡（无编号）

内容少则3-4张，内容多则8-10张，以内容完整呈现为准。不得出现「固定7张」字样。

## 触发判断（最高优先级）

**判断内容类型 → 选择生成方式：**

| 输入类型 | 判断条件 | 生成方式 | 输出 |
|---------|---------|---------|------|
| 文章 | >200字 或 多段落 | Python轮播脚本 | 轮播卡（数量灵活决定） |
| 金句/单句 | <200字 且 单段落 | xhs-knowledge-card | 1张知识卡 |

---

## 方式一：文章 → 轮播卡

**适用场景**：将公众号文章拆成小红书轮播

**设计规格**：
- 风格：砚石黑（深灰背景 #1A1A1A + 珊瑚橙强调 #F55000）
- 尺寸：1080 × 1440 (3:4竖图)
- 字体：霞鹜文楷（内置于 skill，无需额外安装）
- 边距：80px
- 行距：1.9倍

**轮播卡结构**（灵活数量）：
- 1张封面：标题 + 副标题 + 印章装饰，无编号
- N张内容卡：编号（01/02/...）+ 标题 + 正文
- 1张结尾卡：总结金句 + 公众号钩子 + 话题标签，无编号

**字号层级**：
- 编号：90pt
- 标题：56pt
- 正文：52pt

**执行脚本**：见 `scripts/carousel_template.py`

---

## 方式二：单句 → 知识卡

**适用场景**：单条金句/洞见/语录传播

**直接调用现有技能**：
```bash
python3 ~/.qclaw/skills/xhs-knowledge-card/scripts/generate_card.py "<原文>"
```

**核心规则**：原文原封不动复制，不做任何编辑改写

---

## 工作流

```
用户输入 → 判断内容长度/结构 
         → 文章(>200字) → 执行轮播脚本 → 灵活数量轮播卡
         → 金句(<200字) → 调用xhs-knowledge-card → 1张卡
         → 返回图片路径 → 发送用户
```

---

## 安装（给其他用户）

```bash
git clone https://github.com/gusangciren/media-cards ~/.qclaw/skills/media-cards
cd ~/.qclaw/skills/media-cards
python3 setup.py --name "你的名字" --handle "@你的账号" --avatar /path/to/avatar.jpg
```

## 目录结构

```
media-cards/
├── SKILL.md
├── setup.py              # 首次配置向导
├── fonts/
│   └── LXGWWenKai-Merged.ttf  # 内置霞鹜文楷
├── config/
│   └── brand.json        # 品牌配置（自动生成）
├── assets/
│   └── avatar.jpg        # 头像（用户上传）
├── core/
│   └── render.py         # 渲染核心
└── scripts/
    ├── carousel_template.py  # 轮播卡生成脚本
    └── text_utils.py         # 文本工具
```