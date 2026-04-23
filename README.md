<p align="center">
  <img src="assets/sloth-avatar-round.png" width="120" />
</p>

<h1 align="center">Sloth-SMM-Eido</h1>

<p align="center">
  <strong>深声 · 内容运营 Skill（社区版）</strong><br/>
  从选题策划到多平台发布的一站式内容创作流水线
</p>

<p align="center">
  <img src="assets/qrcode.jpg" width="140" /><br/>
  <sub>扫码关注 <strong>树懒老K</strong> · 获取更多 AI 技能</sub><br/>
  <em>慢一点，深一度</em>
</p>

[![QoderWork Skill](https://img.shields.io/badge/QoderWork-Skill-blue)](https://docs.qoder.com/qoderwork/introduction)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]()
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

[English](README_EN.md) | 中文

## 品名释义

> **深声**——「深」取自树懒老K品牌哲学「慢一点，深一度」，「声」意为发声、传播。好内容不是流量噪音，而是有深度的声音。深声，让每一次内容输出都掷地有声、深入人心。

## 简介

Sloth-SMM-Eido 是一个基于 QoderWork 的深声 · 内容运营 SKILL，覆盖从选题策划、内容创作到多平台分发的完整工作流。

**这是社区版（Community Edition）**，已脱敏处理，不含任何个人品牌素材和私有配置。您可以直接使用并根据自己的需求自定义。

## 核心能力

### 三大使用场景

**热点追踪 → 爆文**：自动抓取热点新闻，智能选题评分，一键生成多平台文章。

**专题策划 → 系列文章**：深度调研方向，规划系列选题，批量循环生产。

**主题写作 → 快速分发**：给定主题直接写作，自动适配全平台。

### 五大平台适配

| 平台 | 发布方式 | 特点 |
|------|---------|------|
| 微信公众号 | API/浏览器自动发布到草稿箱 | 主题排版、品牌题图底图、封面图 |
| 今日头条 | Chrome CDP 自动发布到草稿箱 | SEO 关键词优化、算法友好结构 |
| 知乎 | 本地输出，手动发布 | 学术化风格、引用规范 |
| 小红书 | 本地输出 + 图卡生成 | emoji 风格、图卡系列 |
| 朋友圈 | 生成文案，手动发布 | 80 字精炼文案、配图建议 |

### 五大模块

| 模块 | 功能 |
|------|------|
| 选题引擎 | 热点抓取、内容拆解、多维评分、智能推荐 |
| 写作引擎 | 四种风格（深度/故事/犀利/轻松）、素材收集、大纲生成 |
| 平台适配器 | 标题改写、内容改写、平台特有元素 |
| 排版引擎 | 公众号主题排版、AI 配图、小红书图卡 |
| 发布管线 | 自动发草稿、飞书归档、Obsidian 归档 |

## 快速开始

### 安装

将整个目录复制到 `~/.qoderwork/skills/Sloth-SMM-Eido/`，首次使用时 SKILL 会自动引导配置。

### 个性化配置

编辑 `EXTEND.md` 完成以下配置：

1. **内容领域**：设置你关注的领域（科技/成长/商业等）
2. **品牌图**（可选）：将你的品牌题图和底图放入 `assets/` 目录，并在 `wechat_ads` 中配置路径
3. **Obsidian**（可选）：填写 `obsidian.vault_path` 并将 `enabled` 设为 `true`
4. **飞书**（可选）：填写 `feishu.space_id` 并将 `enabled` 设为 `true`
5. **微信 API**：配置 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET` 环境变量

### 前置依赖

核心依赖：`baoyu-post-to-wechat`（公众号发布）、`news-aggregator-skill`（热点抓取）、`deep-research`（深度调研）、`baoyu-article-illustrator`（AI 配图）、`baoyu-xhs-images`（小红书图卡）。

可选依赖：`lark-doc` + `lark-wiki`（飞书归档）、Chrome 浏览器（头条发布）。

### 基本用法

```
# 热点追踪
帮我追踪今天的科技热点，选一个好选题写一篇爆文

# 专题策划
我想做一个关于"AI时代个人成长"的系列专题

# 主题写作
帮我写一篇关于"向上管理"的文章，发布到所有平台
```

## 自定义指南

### 添加品牌图

准备题图和底图（推荐宽度 900-1080px，JPEG/PNG），放入 `assets/` 目录，然后在 `EXTEND.md` 的 `wechat_ads` 中配置路径即可。详见 `assets/README.md`。

### 修改写作风格

在 `EXTEND.md` 中设置 `default_style`，支持 `deep`（深度干货）、`story`（故事情感）、`sharp`（观点犀利）、`light`（轻松科普），或使用 `auto` 让 SKILL 根据选题自动匹配。

### 扩展新平台

在 `platform-styles/` 目录下新增平台风格文件，并在 `modules/platform-adapter.md` 中添加对应适配规则。

## 目录结构

```
Sloth-SMM-Eido/
├── SKILL.md                    # 主指令文件
├── EXTEND.md                   # 用户配置模板
├── .skill-metadata.yaml        # Skill 商店示例
├── assets/                     # 品牌素材（请添加你的品牌图）
│   └── README.md
├── modules/                    # 功能模块
│   ├── topic-engine.md
│   ├── writing-engine.md
│   ├── platform-adapter.md
│   ├── format-engine.md
│   └── publish-pipeline.md
├── platform-styles/            # 平台风格参考
│   ├── wechat.md
│   ├── toutiao.md
│   ├── zhihu.md
│   ├── xiaohongshu.md
│   └── moments.md
├── templates/                  # 写作模板
│   ├── outline-deep.md
│   ├── outline-story.md
│   ├── outline-sharp.md
│   ├── outline-light.md
│   └── topic-card.md
└── scripts/                    # 自动化脚本
    ├── toutiao-publish.py
    └── publish-log.py
```

## 版本记录

详见 [CHANGELOG.md](CHANGELOG.md)。

## 文档

- [用户使用指南](references/user-guide.md) — 完整的功能说明、使用流程与最佳实践

## 版本

当前版本：1.0.0

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
