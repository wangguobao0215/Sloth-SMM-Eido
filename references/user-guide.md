# Sloth-SMM-Eido 用户使用指南

> 版本：1.0.0（社区版） | 适用于 QoderWork 桌面端

## 目录

1. [技能定位](#1-技能定位)
2. [安装与初始化](#2-安装与初始化)
3. [核心功能与命令](#3-核心功能与命令)
4. [使用流程指南](#4-使用流程指南)
5. [最佳实践](#5-最佳实践)
6. [常见问题 (FAQ)](#6-常见问题-faq)
7. [参考索引](#7-参考索引)

---

## 1. 技能定位

Sloth-SMM-Eido 是基于 QoderWork 的 **自媒体全流程运营技能**，覆盖从选题策划、内容创作到多平台分发的完整工作流。本版本为社区版（Community Edition），已脱敏处理，不含个人品牌素材和私有配置，可直接使用和自定义。

**核心价值**：

| 价值点 | 说明 |
|--------|------|
| 全流程覆盖 | 从热点追踪、选题策划到多平台发布，一站式完成 |
| 五平台适配 | 微信公众号、今日头条、知乎、小红书、朋友圈 |
| 模块化架构 | 选题/写作/适配/排版/发布五大模块，按需调用 |
| 多种写作风格 | 深度干货、故事情感、观点犀利、轻松科普四种风格 |
| 自动化发布 | 公众号 API/浏览器发布、头条 CDP 发布、飞书/Obsidian 归档 |

**适用人群**：

- 自媒体运营者 / 内容创作者
- 企业新媒体团队
- 个人品牌建设者
- 需要多平台分发的内容生产者

---

## 2. 安装与初始化

### 2.1 安装步骤

1. 将整个 `Sloth-SMM-Eido/` 目录复制到 `~/.qoderwork/skills/Sloth-SMM-Eido/`
2. 首次使用时，技能会自动引导你完成配置

### 2.2 首次配置（EXTEND.md）

首次启动时，技能会通过交互式问答引导你配置以下内容，结果会写入 `EXTEND.md`：

| 配置项 | 说明 | 是否必填 |
|--------|------|---------|
| 内容领域 | 科技/成长/商业/混合 | 必填 |
| 常用平台 | 公众号/头条/知乎/小红书/朋友圈（开关） | 必填 |
| 飞书知识库 | space_id，用于归档到飞书 Wiki | 可选 |
| Obsidian vault 路径 | 本地知识库路径，用于归档 | 可选 |
| 微信发布方式 | api（推荐）或 browser | 必填 |

你也可以随时手动编辑 `EXTEND.md` 修改配置。

### 2.3 前置依赖

**核心依赖**（必装）：

| 依赖 | 用途 |
|------|------|
| `baoyu-post-to-wechat` | 微信公众号排版与发布 |
| `news-aggregator-skill` | 热点新闻抓取 |
| `deep-research` | 深度调研 |
| `baoyu-article-illustrator` | AI 长文配图 |
| `baoyu-xhs-images` | 小红书图卡生成 |

**可选依赖**：

| 依赖 | 用途 |
|------|------|
| `lark-doc` + `lark-wiki` | 飞书文档归档 |
| Chrome 浏览器 | 今日头条 CDP 自动发布 |

### 2.4 环境变量（公众号 API 模式）

如使用公众号 API 发布模式，需配置：
- `WECHAT_APP_ID` — 微信公众号 AppID
- `WECHAT_APP_SECRET` — 微信公众号 AppSecret

---

## 3. 核心功能与命令

### 3.1 三大使用场景

| 场景 | 触发信号 | 说明 |
|------|---------|------|
| 热点追踪 | "热点"、"追踪"、"今天有什么"、"爆文" | 自动抓取热点 -> 选题评分 -> 写作 -> 适配 -> 发布 |
| 专题策划 | "策划"、"专题"、"系列"、"合集" | 深度调研 -> 系列选题 -> 循环写作 -> 批量发布 |
| 主题写作 | 给出明确主题或标题 | 跳过选题 -> 直接写作 -> 适配 -> 发布 |

### 3.2 五大功能模块

| 模块 | 功能 | 详细指令 |
|------|------|---------|
| 选题引擎 | 热点抓取、内容拆解、多维评分、智能推荐 | [modules/topic-engine.md](../modules/topic-engine.md) |
| 写作引擎 | 四种风格写作、素材收集、大纲生成、全文创作 | [modules/writing-engine.md](../modules/writing-engine.md) |
| 平台适配器 | 标题改写（每平台3个候选）、内容改写、平台特有元素 | [modules/platform-adapter.md](../modules/platform-adapter.md) |
| 排版引擎 | 公众号主题排版、AI 配图、小红书图卡 | [modules/format-engine.md](../modules/format-engine.md) |
| 发布管线 | 自动发草稿、飞书归档、Obsidian 归档、发布日志 | [modules/publish-pipeline.md](../modules/publish-pipeline.md) |

### 3.3 五大平台适配

| 平台 | 发布方式 | 风格特点 | 风格参考 |
|------|---------|---------|---------|
| 微信公众号 | API/浏览器自动发布到草稿箱 | 主题排版、品牌题图、封面图 | [platform-styles/wechat.md](../platform-styles/wechat.md) |
| 今日头条 | Chrome CDP 自动发布到草稿箱 | SEO 关键词优化、算法友好结构 | [platform-styles/toutiao.md](../platform-styles/toutiao.md) |
| 知乎 | 本地输出，手动发布 | 学术化风格、引用规范 | [platform-styles/zhihu.md](../platform-styles/zhihu.md) |
| 小红书 | 本地输出 + 图卡生成 | emoji 风格、图卡系列 | [platform-styles/xiaohongshu.md](../platform-styles/xiaohongshu.md) |
| 朋友圈 | 生成文案，手动发布 | 80字精炼文案、配图建议 | [platform-styles/moments.md](../platform-styles/moments.md) |

### 3.4 四种写作风格

| 风格 | 代码 | 特点 | 大纲模板 |
|------|------|------|---------|
| 深度干货 | `deep` | 数据支撑、结构严谨、专业深入 | [templates/outline-deep.md](../templates/outline-deep.md) |
| 故事情感 | `story` | 叙事驱动、情感共鸣、场景化 | [templates/outline-story.md](../templates/outline-story.md) |
| 观点犀利 | `sharp` | 立场鲜明、逻辑锋利、争议性 | [templates/outline-sharp.md](../templates/outline-sharp.md) |
| 轻松科普 | `light` | 通俗易懂、比喻丰富、轻松阅读 | [templates/outline-light.md](../templates/outline-light.md) |

可在 `EXTEND.md` 中设置 `default_style`，或使用 `auto` 让技能根据选题自动匹配。

---

## 4. 使用流程指南

### 4.1 场景一：热点追踪 -> 爆文

```
Step 1  选题引擎（热点模式）
        "帮我追踪今天的科技热点，选一个好选题写一篇爆文"
        → 调用 news-aggregator 抓取热点
        → 生成选题卡片 + 评分排序
        → 你选择最佳选题

Step 2  写作引擎
        → 自动推荐风格（你可以修改）
        → 生成大纲（你审核调整）
        → 全文写作 + 润色自检
        → 输出母版文章（master.md）

Step 3  平台适配器
        → 读取 EXTEND.md 中开启的平台
        → 逐平台改写标题（每平台3个候选）+ 改写内容
        → 输出各平台版本

Step 4  排版引擎
        → 公众号：主题排版 + 品牌图
        → 长文平台：AI 自动配图
        → 小红书：生成图卡系列

Step 5  发布管线
        → 公众号：发布到草稿箱
        → 头条：CDP 自动发布到草稿箱
        → 飞书：归档到知识库
        → Obsidian：复制到本地 vault
        → 知乎/小红书：保存到输出目录
        → 朋友圈：生成 moments.md
        → 记录发布日志
```

### 4.2 场景二：专题策划 -> 系列文章

```
Step 1  选题引擎（策划模式）
        "我想做一个关于'AI时代个人成长'的系列专题"
        → 调用 deep-research 调研方向
        → 生成 3-5 个专题方案
        → 你选择专题 → 拆分为系列选题（每专题 3-8 篇）
        → 排定写作顺序

Step 2-N  循环执行（每篇文章）
        写作引擎 → 平台适配器 → 排版引擎 → 发布管线
        每篇完成后你可以选择：
        - 继续下一篇
        - 修改当前文章
        - 调整后续计划
        - 暂停，稍后继续
```

### 4.3 场景三：主题写作 -> 快速分发

```
Step 1  接收主题
        "帮我写一篇关于'向上管理'的文章，发布到所有平台"
        → 跳过选题引擎，直接进入写作

Step 2-5  同场景一的 Step 2-5
```

### 4.4 文件输出结构

所有生成文件统一存放到用户工作目录：

```
{输出目录}/
├── {日期}_{主题slug}/
|   ├── master.md              # 母版文章
|   ├── wechat.md              # 公众号适配版
|   ├── toutiao.md             # 今日头条适配版
|   ├── zhihu.md               # 知乎适配版
|   ├── xiaohongshu.md         # 小红书文案
|   ├── moments.md             # 朋友圈文案 + 配图建议
|   ├── images/                # 配图目录
|   └── xhs-images/            # 小红书图卡目录
└── publish-log.json           # 发布日志
```

---

## 5. 最佳实践

### 5.1 选题与写作

- **热点要快**：热点追踪类内容时效性强，建议发现热点后 2-4 小时内完成全流程
- **专题要深**：系列专题重质量不重速度，每篇认真审核大纲后再生成全文
- **风格要匹配**：不确定风格时使用 `auto` 模式，让技能根据选题特征自动推荐

### 5.2 平台适配

- **标题差异化**：每个平台的标题风格不同（公众号悬念型、头条 SEO 型、小红书 emoji 型），不要跨平台使用同一标题
- **内容有侧重**：知乎偏学术引用，小红书偏视觉化表达，朋友圈要控制在 80 字内
- **先审后发**：自动发布到草稿箱后，建议在各平台后台预览确认再正式发布

### 5.3 品牌建设

- **统一品牌图**：准备品牌题图和底图（900-1080px 宽），放入 `assets/` 并在 `EXTEND.md` 配置
- **知识归档**：开启飞书或 Obsidian 归档，长期积累形成内容知识库
- **发布日志**：定期查看 `publish-log.json`，分析发布频率和平台覆盖情况

### 5.4 效率提升

- **批量生产**：专题策划模式支持循环生产系列文章，适合周末集中创作
- **模板复用**：熟悉四种大纲模板后，可以快速调整大纲结构
- **关键节点确认**：选题选择、风格确认、大纲审核、标题选择这四个环节需要你确认，其余自动完成

---

## 6. 常见问题 (FAQ)

### Q1：首次使用时 EXTEND.md 配置出错了，可以重新配置吗？

可以。直接编辑 `EXTEND.md` 文件修改配置项即可。也可以删除 `EXTEND.md` 后重新开始对话，技能会再次引导你完成配置。

### Q2：公众号发布失败，提示 API 认证错误怎么办？

请检查以下几点：
1. 确认 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET` 环境变量已正确设置
2. 确认公众号已开通开发者权限
3. 如 API 模式不可用，可在 `EXTEND.md` 中将发布方式切换为 `browser` 模式

### Q3：头条自动发布需要什么前置条件？

需要以 `--remote-debugging-port=9222` 参数启动 Chrome 浏览器，并在浏览器中登录 mp.toutiao.com。技能通过 Chrome DevTools Protocol (CDP) 实现自动化发布。

### Q4：可以自定义新的写作风格吗？

当前版本支持四种内置风格（deep/story/sharp/light）。如需自定义，可在 `templates/` 目录下参考现有大纲模板创建新模板，并在 `modules/writing-engine.md` 中添加对应风格定义。

### Q5：如何扩展支持新的发布平台？

1. 在 `platform-styles/` 目录下创建新平台的风格参考文件（如 `douyin.md`）
2. 在 `modules/platform-adapter.md` 中添加对应的适配规则
3. 如需自动发布，在 `scripts/` 目录下编写发布脚本，并在 `modules/publish-pipeline.md` 中注册

---

## 7. 参考索引

### 功能模块（modules/）

| 文件 | 内容 |
|------|------|
| [topic-engine.md](../modules/topic-engine.md) | 选题引擎 — 热点抓取、内容拆解、多维评分 |
| [writing-engine.md](../modules/writing-engine.md) | 写作引擎 — 四种风格、素材收集、大纲生成、全文创作 |
| [platform-adapter.md](../modules/platform-adapter.md) | 平台适配器 — 标题改写、内容改写、平台特有元素 |
| [format-engine.md](../modules/format-engine.md) | 排版引擎 — 公众号排版、AI 配图、小红书图卡 |
| [publish-pipeline.md](../modules/publish-pipeline.md) | 发布管线 — 自动发布、飞书归档、Obsidian 归档 |

### 平台风格参考（platform-styles/）

| 文件 | 平台 |
|------|------|
| [wechat.md](../platform-styles/wechat.md) | 微信公众号风格规范 |
| [toutiao.md](../platform-styles/toutiao.md) | 今日头条风格规范 |
| [zhihu.md](../platform-styles/zhihu.md) | 知乎风格规范 |
| [xiaohongshu.md](../platform-styles/xiaohongshu.md) | 小红书风格规范 |
| [moments.md](../platform-styles/moments.md) | 朋友圈风格规范 |

### 写作模板（templates/）

| 文件 | 内容 |
|------|------|
| [outline-deep.md](../templates/outline-deep.md) | 深度干货大纲模板 |
| [outline-story.md](../templates/outline-story.md) | 故事情感大纲模板 |
| [outline-sharp.md](../templates/outline-sharp.md) | 观点犀利大纲模板 |
| [outline-light.md](../templates/outline-light.md) | 轻松科普大纲模板 |
| [topic-card.md](../templates/topic-card.md) | 选题卡片模板 |

### 自动化脚本（scripts/）

| 文件 | 功能 |
|------|------|
| [toutiao-publish.py](../scripts/toutiao-publish.py) | 今日头条 CDP 自动发布脚本 |
| [publish-log.py](../scripts/publish-log.py) | 发布日志管理脚本 |

### 其他文件

| 文件 | 内容 |
|------|------|
| [EXTEND.md](../EXTEND.md) | 用户个性化配置模板 |
| [CHANGELOG.md](../CHANGELOG.md) | 版本变更历史 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | 贡献指南 |

---

> 如有问题或建议，欢迎关注 **树懒老K** 交流反馈。
