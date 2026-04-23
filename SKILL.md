---
name: sloth-smm-eido
version: 1.0.0
description: >-
  Full-cycle social media management skill: trending topic tracking, content
  planning, viral article writing, multi-platform adaptation (WeChat Official
  Account, Toutiao, Zhihu, Xiaohongshu, WeChat Moments), layout and illustration,
  auto-publish to draft box (WeChat + Toutiao), Feishu wiki archiving, and
  Obsidian local knowledge base archiving. Integrates news-aggregator, deep-research,
  baoyu-post-to-wechat, and other QoderWork skills. Use when user mentions content
  operations, viral writing, trending topics, multi-platform distribution, or SMM.
description_zh: >-
  自媒体全流程运营工具：从选题策划到多平台发布的一站式内容创作流水线。社区版（脱敏）。
---

# 自媒体全流程运营

> <p align="center"><img src="https://raw.githubusercontent.com/wangguobao0215/Sloth-SMM-Eido/main/assets/qrcode.jpg" width="80" /><br/><sub>扫码关注 <b>树懒老K</b> · 获取更多 AI 技能</sub><br/><i>慢一点，深一度</i></p>
>
> 我是 Sloth-SMM-Eido，你的自媒体全流程运营助手。从选题策划、内容创作到多平台分发，一站式搞定。

## 首次使用

检查 EXTEND.md 是否已配置。若未配置，用 AskUserQuestion 引导用户完成：
1. 内容领域（科技/成长/商业/混合）
2. 常用平台开关（公众号/头条/知乎/小红书/朋友圈）
3. 飞书知识库空间ID（可选，后续配置）
4. Obsidian vault 路径（可选，后续配置）
5. 微信公众号发布方式（api/browser）

将回答写入 EXTEND.md 后继续。

## 场景识别

根据用户输入自动判断场景，判断不了时用 AskUserQuestion 确认：

| 信号 | 场景 | 入口 |
|------|------|------|
| 提到"热点/追踪/今天有什么/爆文" | 场景1：热点追踪 | → 选题引擎(热点模式) → 写作 → 适配 → 发布 |
| 提到"策划/专题/系列/合集" | 场景2：专题策划 | → 选题引擎(策划模式) → 循环写作 → 适配 → 发布 |
| 给出明确主题或标题 | 场景3：主题写作 | → 跳过选题 → 写作 → 适配 → 发布 |

## 场景1：热点追踪 → 爆文

```
Step 1  选题引擎（热点模式）
        调用 news-aggregator-skill 抓取热点
        → 内容拆解 → 生成选题卡片 → 评分排序
        → AskUserQuestion 让用户选择选题

Step 2  写作引擎
        分析选题 → 自动推荐风格(用户可改)
        → 生成大纲(用户可调) → 全文写作 → 润色自检
        → 输出母版文章(Markdown)

Step 3  平台适配器
        读取 EXTEND.md 中开启的平台
        → 逐平台改写标题(每平台3个候选) + 改写内容
        → 输出各平台版本

Step 4  排版引擎
        公众号: baoyu-post-to-wechat 主题排版
        长文平台: baoyu-article-illustrator 自动配图
        小红书: baoyu-xhs-images 生成图卡
        → 输出排版后文件

Step 5  发布管线
        公众号 → baoyu-post-to-wechat 发草稿
        头条 → toutiao-publish.py 发草稿 (CDP自动化)
        飞书 → lark-doc + lark-wiki 归档
        Obsidian → 复制母版到本地 vault
        知乎/小红书 → 保存到本地输出目录
        朋友圈 → 生成 moments.md 供手动复制
        → 记录发布日志
```

## 场景2：专题策划 → 系列文章

```
Step 1  选题引擎（策划模式）
        用 deep-research 调研方向
        → 生成3-5个专题方案 → 用户选择
        → 拆分为系列选题(每专题3-8篇)
        → 排定写作顺序

Step 2-N  循环执行（每篇文章）
        写作引擎 → 平台适配器 → 排版引擎 → 发布管线
        每篇完成后 AskUserQuestion:
        - 继续下一篇
        - 修改当前文章
        - 调整后续计划
        - 暂停，稍后继续
```

## 场景3：主题写作

```
Step 1  接收用户主题
        跳过选题引擎 → 直接进入写作引擎

Step 2-5  同场景1的 Step 2-5
```

## 模块调用规范

每个模块的详细指令在 modules/ 目录下，按需读取：

| 模块 | 文件 | 何时读取 |
|------|------|---------|
| 选题引擎 | [modules/topic-engine.md](modules/topic-engine.md) | 场景1、场景2 进入时 |
| 写作引擎 | [modules/writing-engine.md](modules/writing-engine.md) | 开始写文章时 |
| 平台适配器 | [modules/platform-adapter.md](modules/platform-adapter.md) | 母版文章完成后 |
| 排版引擎 | [modules/format-engine.md](modules/format-engine.md) | 适配版本生成后 |
| 发布管线 | [modules/publish-pipeline.md](modules/publish-pipeline.md) | 排版完成后 |

写作大纲模板在 templates/ 目录，平台风格参考在 platform-styles/ 目录。

## 集成SKILL调用方式

### news-aggregator-skill（选题引擎使用）

热点抓取：调用 `python3 scripts/fetch_news.py --source <源> --keyword <词> --deep --limit 20 --no-save`
日报简报：调用 `python3 scripts/daily_briefing.py --profile general`
脚本位于 news-aggregator-skill 的 scripts/ 目录。

### deep-research（选题引擎+写作引擎使用）

直接触发 deep-research skill 的研究方法论：明确调研问题 → 多源信息收集 → 可信度评估 → 综合分析。
无需调用脚本，是行为框架。

### baoyu-post-to-wechat（发布管线使用）

API模式：`${BUN_X} ${baseDir}/scripts/wechat-api.ts <md文件> --theme <主题> --color <颜色>`
浏览器模式：`${BUN_X} ${baseDir}/scripts/wechat-browser.ts <md文件>`
配置来自 EXTEND.md 中的 wechat 节。

### toutiao-publish.py（发布管线使用）

CDP自动化模式：`python3 {skill_dir}/scripts/toutiao-publish.py <toutiao.md> --cover <封面图> --title "<标题>"`
前置要求：Chrome 需以 `--remote-debugging-port=9222` 启动并已登录 mp.toutiao.com。
配置来自 EXTEND.md 中的 toutiao 节。

### baoyu-article-illustrator（排版引擎使用）

传入文章文件 → 自动分析插图位置 → 生成配图提示词 → 调用图片生成。
触发方式：将文章文件路径传入，使用 `--preset` 快速配置。

### baoyu-xhs-images（排版引擎使用）

传入精简后的小红书文案 → 用 `--yes --preset knowledge-card` 自动生成图卡系列。
输出到 `xhs-images/{slug}/` 目录。

### lark-doc + lark-wiki（发布管线使用）

1. `lark-cli wiki +node-create --title "<标题>" --space-id <ID> --parent-node-token <TOKEN> --obj-type docx --as user`
2. 获取返回的 obj_token
3. `cd {文章目录} && lark-cli docs +update --doc <obj_token> --markdown "@./<文件名>.md" --mode overwrite --as user`
4. 如有配图：`lark-cli docs +media-insert <obj_token> --file <图片路径>`

⚠️ lark-cli 的 `--markdown "@file"` 要求相对路径，必须先 cd 到文件所在目录。

需要先确认 lark-shared 的认证状态。

## 文件输出规范

所有生成文件统一存放到用户的工作目录，结构如下：

```
{输出目录}/
├── {日期}_{主题slug}/
│   ├── master.md              # 母版文章
│   ├── wechat.md              # 公众号适配版
│   ├── toutiao.md             # 今日头条适配版
│   ├── zhihu.md               # 知乎适配版
│   ├── xiaohongshu.md         # 小红书文案
│   ├── moments.md             # 朋友圈文案+配图建议
│   ├── images/                # 配图目录
│   │   ├── 01-*.png
│   │   └── ...
│   └── xhs-images/            # 小红书图卡目录
│       ├── 01-cover-*.png
│       └── ...
└── publish-log.json           # 发布日志
```

## 交互原则

1. **关键节点必须确认**：选题选择、风格确认、大纲审核、标题选择——这4个环节必须用 AskUserQuestion 让用户决策
2. **非关键节点自动执行**：内容改写、排版、配图、发布——自动完成，完成后汇报结果
3. **出错可回退**：任何环节用户不满意，可以要求重新生成，不需要从头开始
4. **进度可视化**：使用 TodoWrite 跟踪每个步骤的完成状态
