# Sloth-SMM-Eido — 深声 · 内容运营 (Community Edition)

> End-to-end Social Media Management SKILL (深声 · 内容运营) — An all-in-one content creation pipeline from topic planning to multi-platform distribution (Community Edition)

[![QoderWork Skill](https://img.shields.io/badge/QoderWork-Skill-blue)](https://docs.qoder.com/qoderwork/introduction)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]()
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

English | [中文](README.md)

## Introduction

Sloth-SMM-Eido is a QoderWork-based social media management SKILL that covers the complete workflow from topic planning and content creation to multi-platform distribution.

**This is the Community Edition**, desensitized and free of any personal brand assets or private configurations. You can use it directly and customize it to your needs.

## Core Capabilities

### Three Usage Scenarios

**Hot Topic Tracking → Viral Article**: Automatically fetches trending news, scores topics intelligently, and generates multi-platform articles.

**Series Planning → Article Series**: Deep-researches a direction, plans a series of topics, and batch-produces articles.

**Topic-Based Writing → Quick Distribution**: Writes from a given topic and auto-adapts for all platforms.

### Five Platform Adapters

| Platform | Publishing Method | Features |
|----------|------------------|----------|
| WeChat Official Account (微信公众号) | API/Browser auto-publish to drafts | Theme formatting, brand images, cover |
| Toutiao (今日头条) | Chrome CDP auto-publish to drafts | SEO optimization, algorithm-friendly |
| Zhihu (知乎) | Local output, manual publish | Academic style, citations |
| Xiaohongshu (小红书) | Local output + image cards | Emoji style, image series |
| WeChat Moments (朋友圈) | Generated copy, manual publish | 80-char concise copy |

### Five Core Modules

| Module | Function |
|--------|----------|
| Topic Engine | Hot topic fetching, content analysis, scoring, recommendations |
| Writing Engine | Four styles (deep/story/sharp/light), material collection, outline generation |
| Platform Adapter | Title rewriting, content adaptation, platform-specific elements |
| Format Engine | WeChat theme formatting, AI illustrations, Xiaohongshu image cards |
| Publish Pipeline | Auto-draft publishing, Feishu/Obsidian archiving |

## Quick Start

### Installation

Copy the entire directory to `~/.qoderwork/skills/Sloth-SMM-Eido/`. The SKILL will guide you through configuration on first use.

### Customization

Edit `EXTEND.md` to configure:

1. **Content domains**: Set your focus areas (tech, growth, business, etc.)
2. **Brand images** (optional): Place your brand header/footer images in `assets/` and set paths in `wechat_ads`
3. **Obsidian** (optional): Set `obsidian.vault_path` and enable
4. **Feishu** (optional): Set `feishu.space_id` and enable
5. **WeChat API**: Configure `WECHAT_APP_ID` and `WECHAT_APP_SECRET` environment variables

### Prerequisites

Core: `baoyu-post-to-wechat`, `news-aggregator-skill`, `deep-research`, `baoyu-article-illustrator`, `baoyu-xhs-images`.

Optional: `lark-doc` + `lark-wiki` (Feishu archiving), Chrome browser (Toutiao publishing).

### Basic Usage

```
# Hot topic tracking
Track today's tech hot topics, pick a good one and write a viral article

# Series planning
I want to create a series on "Personal Growth in the AI Era"

# Topic-based writing
Write an article about "upward management", publish to all platforms
```

## Customization Guide

### Adding Brand Images

Prepare header and footer images (recommended width 900-1080px, JPEG/PNG), place them in `assets/`, and configure paths in `EXTEND.md` under `wechat_ads`. See `assets/README.md` for specifications.

### Changing Writing Style

Set `default_style` in `EXTEND.md`: `deep` (in-depth), `story` (narrative), `sharp` (opinion), `light` (casual explainer), or `auto` (recommended, auto-matches based on topic).

### Adding New Platforms

Create a new platform style file in `platform-styles/` and add corresponding adaptation rules in `modules/platform-adapter.md`.

## Directory Structure

```
Sloth-SMM-Eido/
├── SKILL.md                    # Main instructions
├── EXTEND.md                   # User config template
├── assets/                     # Brand assets (add your own)
│   └── README.md
├── modules/                    # Functional modules
├── platform-styles/            # Platform style references
├── templates/                  # Writing outline templates
└── scripts/                    # Automation scripts
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Documentation

- [User Guide](references/user-guide.md) — Complete feature guide, workflows, and best practices (Chinese)

## Version

Current version: 1.0.0

## License

This project is licensed under the [MIT License](LICENSE).
