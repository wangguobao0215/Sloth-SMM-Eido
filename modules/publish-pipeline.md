# 模块E：发布管线 (Publish Pipeline)

## 概述

将排版完成的文章发布到各个平台的草稿箱，归档到飞书知识库和本地 Obsidian 知识库。

## 发布流程

```
读取各平台排版后文件
→ 检查各平台发布条件
→ 公众号: baoyu-post-to-wechat 发布草稿
→ 头条: toutiao-publish.py 发布草稿 (CDP自动化)
→ 飞书: lark-doc + lark-wiki 创建文档并归档
→ Obsidian: 复制母版文章到本地 vault
→ 知乎/小红书: 保存到输出目录
→ 朋友圈: 生成 moments.md 供手动复制
→ 记录发布日志
→ 汇报发布结果
```

## 微信公众号发布

### 品牌图（题图 & 底图）— 强制规则

**如果 EXTEND.md 中配置了品牌题图和底图，所有公众号文章必须使用统一的品牌题图和底图。禁止为每篇文章单独生成题图/底图。**

品牌图源文件路径来自 EXTEND.md 的 `wechat_ads` 配置：
- 题图: `wechat_ads.header_image`
- 底图: `wechat_ads.footer_image`

在生成每篇文章的平台版本时，如果品牌图已配置，必须执行以下操作：
```bash
# 从配置路径复制品牌图到文章 images 目录（不是生成新图！）
cp "{header_image路径}" "{article_dir}/images/{header_image文件名}"
cp "{footer_image路径}" "{article_dir}/images/{footer_image文件名}"
```

wechat.md 中的引用格式：
```markdown
# 标题

![题图](images/{header_image文件名})

...正文...

![底图](images/{footer_image文件名})
```

**严禁用 ImageGen 或任何方式为题图/底图生成新图片。** 如果配置了品牌图路径但文件不存在，应报错并提示用户检查 assets 目录，而不是自行生成替代品。如果未配置品牌图（路径为空），则跳过此步骤。

### 前置检查

1. 确认 EXTEND.md 中 wechat 配置完整
2. 如果使用 API 模式：确认 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量存在
3. 如果使用 Browser 模式：确认 Chrome 已安装
4. **如果配置了品牌图路径，确认对应文件存在**

### 封面图

微信 API 模式发布草稿**必须提供封面图**，否则会报错。

封面图获取优先级：
1. 文章配图中的第一张（images/01-*.png）
2. 如果没有配图，用 ImageGen 生成封面图（16:9 横版，科技感/商业感风格，包含文章核心概念）
3. 保存到 `images/cover.png`

### 发布命令

```bash
# 定位 baoyu-post-to-wechat 的脚本目录
# 查找: ~/.qoderwork/skills/baoyu-post-to-wechat/scripts/
# 或: ~/.agents/skills/baoyu-post-to-wechat/scripts/

# API 模式（--cover 参数指定封面图）
${BUN_X} {post_to_wechat_dir}/scripts/wechat-api.ts \
  {wechat.md路径} \
  --theme {EXTEND.md中的theme} \
  --color {EXTEND.md中的color} \
  --author "{EXTEND.md中的author}" \
  --cover {封面图路径} \
  --type article

# Browser 模式
${BUN_X} {post_to_wechat_dir}/scripts/wechat-browser.ts \
  {wechat.md路径}
```

### 发布结果

成功后记录返回的 media_id 和发布状态。

注意：此步骤只是创建草稿，不会直接发布。用户需要到 mp.weixin.qq.com 确认后发布。

---

## 今日头条发布（CDP 自动化）

### 前置检查

1. 确认 EXTEND.md 中 toutiao.enabled 为 true
2. 确认 Chrome 已启动并开启远程调试：`chrome.exe --remote-debugging-port=9222`
3. 确认已在 Chrome 中手动登录 mp.toutiao.com（cookie 有效期约 7 天）

### 发布命令

```bash
# 设置编码（Windows 兼容）
set PYTHONIOENCODING=utf-8

# 发布到头条草稿箱
python3 {skill_dir}/scripts/toutiao-publish.py \
  {toutiao.md路径} \
  --cover {封面图路径} \
  --title "{文章标题}"
```

### 封面图

头条封面图获取优先级（与公众号共用）：
1. 文章配图中的第一张（images/01-*.png）
2. 公众号封面图（images/cover.png）
3. 如果都没有，用 ImageGen 生成

### 发布结果

脚本输出 JSON 结果，记录 success/title/status 字段。

注意：
- 此步骤只是保存到草稿箱，不会直接发布。用户需到 mp.toutiao.com 确认后发布
- 如果 Chrome 未启动或未登录，脚本会给出明确的错误提示
- 保存到草稿箱不会触发手机验证（直接发布才会）
- Cookie 过期后需重新在 Chrome 中手动登录 mp.toutiao.com

### 错误处理

- 如果连接 Chrome 失败：提示用户启动 Chrome 并开启 `--remote-debugging-port=9222`
- 如果未登录：提示用户在 Chrome 中手动登录 mp.toutiao.com
- 如果编辑器元素找不到：头条可能更新了页面结构，需更新脚本中的选择器

---

## 飞书知识库归档

### 前置检查

1. 确认 lark-cli 已安装且已认证（`lark-cli auth login`）
2. 确认 EXTEND.md 中 feishu 配置（space_id, parent_node）
3. 如果 space_id 为空且 identity 为 user，使用个人知识库

### 归档流程

支持两种模式（取决于 EXTEND.md 中 feishu 配置）：

**模式A：统一归档** — 一个 space_id + 一个 parent_node，所有平台版本归到同一知识库节点下
**模式B：分平台归档** — EXTEND.md 中为每个平台配置独立的 space_id / parent_node，分别归档

```bash
# Step 1: 为每个平台创建知识库节点
lark-cli wiki +node-create \
  --title "{平台名}专题文章" \
  --space-id "{对应space_id}" \
  --parent-node-token "{对应parent_node}" \
  --obj-type docx \
  --as user

# 返回 node_token 和 obj_token，记录 obj_token

# Step 2: 写入平台适配版内容
# ⚠️ 重要: lark-cli --markdown "@file" 要求相对路径，需先 cd 到文章目录
cd "{文章输出目录}" && \
lark-cli docs +update \
  --doc {obj_token} \
  --markdown "@{平台版本文件名}.md" \
  --mode overwrite \
  --as user

# Step 3: 如有配图，插入媒体
# 对 images/ 目录下每张图片：
lark-cli docs +media-insert {obj_token} --file {图片路径}
```

### 错误处理

- 如果 `--markdown @file` 报路径错误：确认已 cd 到文件所在目录，使用相对路径如 `@./wechat.md`
- 如果 permission denied：提示用户检查 lark-shared 认证和权限配置
- 如果 space_id 无效：用 `lark-cli wiki +space-list` 列出可用空间，让用户选择
- 如果网络超时：等待5秒后重试1次

---

## 知乎/小红书/朋友圈（本地输出）

知乎和小红书暂无自动发布能力，朋友圈无 API，将排版好的文件保存到输出目录，供用户手动发布。

### 输出文件整理

确保以下文件已生成并保存到 `{输出目录}/{日期}_{slug}/`：

```
zhihu.md            ← 知乎版本（直接复制粘贴即可）
xiaohongshu.md      ← 小红书文案
moments.md          ← 朋友圈文案 + 配图建议
xhs-images/         ← 小红书图卡系列
images/             ← 文章配图
```

### 发布提示

向用户提供简明的手动发布指引：

```
知乎：
1. 打开 zhuanlan.zhihu.com → 写文章
2. 复制 zhihu.md 内容粘贴
3. 上传配图
4. 添加话题标签后发布

小红书：
1. 打开小红书APP或Creator Center
2. 上传 xhs-images/ 中的图卡（按序号排列）
3. 复制 xiaohongshu.md 作为正文
4. 添加话题标签后发布

朋友圈：
1. 打开 moments.md，复制文案部分
2. 按 moments.md 中的配图建议选择图片
3. 发朋友圈：粘贴文案 + 选择图片
4. 公众号文章发布后，也可直接分享文章到朋友圈
```

---

## Obsidian 本地知识库归档

### 前置检查

1. 确认 EXTEND.md 中 obsidian.enabled 为 true
2. 确认 obsidian.vault_path 已配置且目录存在
3. 确认目标子目录（obsidian.folder）存在，不存在则自动创建

### 目录结构规则

Obsidian 归档母版文章（master.md）以及需要手动发布的平台版本（知乎、小红书、朋友圈）。
公众号和头条已通过自动化发到草稿箱，不归档其适配版本。

目录按专题组织，每篇文章一个子文件夹：

```
{vault_path}/{folder}/
├── {专题名称}/                      ← 专题系列文章
│   ├── _专题规划.md                 ← 系列规划文档
│   ├── 00_总纲·认知天花板/           ← 每篇文章一个文件夹（中文命名）
│   │   ├── master.md                ← 母版文章（带 YAML frontmatter）
│   │   ├── zhihu.md                 ← 知乎版（手动发布用）
│   │   ├── xiaohongshu.md           ← 小红书文案（手动发布用）
│   │   ├── moments.md               ← 朋友圈文案（手动发布用）
│   │   └── images/                  ← 封面图 + 正文配图
│   │       ├── cover.png
│   │       ├── 01-xxx.png
│   │       └── ...
│   ├── 01_达克效应/
│   │   ├── master.md
│   │   ├── zhihu.md
│   │   ├── xiaohongshu.md
│   │   ├── moments.md
│   │   └── images/
│   └── ...
├── 独立文章/                        ← 非专题的单篇文章（场景1、场景3）
│   ├── {date}_{中文主题}/
│   │   ├── master.md
│   │   ├── zhihu.md
│   │   ├── xiaohongshu.md
│   │   ├── moments.md
│   │   └── images/
│   └── ...
```

**注意**：
- wechat.md 和 toutiao.md **不归档**到 Obsidian（已自动发到草稿箱）
- 每篇文章独立文件夹，**文件夹用中文命名**，格式：`{series_index:02d}_{中文简称}`
- images/ 在每篇文章自己的文件夹内，不共用

### 归档流程

```
1. 读取 EXTEND.md → obsidian 配置
2. 判断文章归属：
   - 如果 master.md frontmatter 中有 series 字段 → 专题文章
     目标目录: {vault_path}/{folder}/{series}/{series_index:02d}_{slug}/
   - 如果没有 series 字段 → 独立文章
     目标目录: {vault_path}/{folder}/独立文章/{date}_{slug}/
3. 如果目标目录不存在，自动创建（含 images/ 子目录）
4. 复制以下文件到目标目录：
   a. master.md — 母版文章（确保 YAML frontmatter 完整）
   b. zhihu.md — 知乎适配版
   c. xiaohongshu.md — 小红书文案
   d. moments.md — 朋友圈文案
   e. images/ 目录下的封面图和正文配图（不含品牌图）
5. master.md 的 YAML frontmatter 确保包含：
   ---
   title: "{文章标题}"
   date: {发布日期 YYYY-MM-DD}
   series: "{系列名称，如有}"
   series_index: {系列编号，如有}
   style: {写作风格}
   platforms: [wechat, toutiao, zhihu, xiaohongshu, moments]
   tags: [{从文章内容提取的3-5个标签}]
   source: "{工作目录中该文章的完整路径}"
   ---
6. 更新所有 md 文件中的图片路径为 Obsidian 相对路径 ./images/xxx.png
7. **不归档** wechat.md 和 toutiao.md（已自动发到草稿箱，无需手动处理）
8. 如果是场景2（专题系列）且 _专题规划.md 尚不存在：
   - 将系列规划文档同步到专题目录根下（不在文章子文件夹内）
```

### 配图处理

默认使用标准 Markdown 图片语法（相对路径），不改为双链格式。
如果用户偏好双链格式，可在 EXTEND.md 中设置 `obsidian.wikilinks: true`。

### 错误处理

- 如果 vault_path 不存在：提示用户检查路径配置
- 如果文件已存在：在文件名后追加时间戳避免覆盖
- 如果图片复制失败：跳过图片，正文中保留原始路径，提示用户手动处理

---

## 发布日志

每次发布操作完成后，调用日志脚本记录结果：

```bash
python3 {skill_dir}/scripts/publish-log.py \
  --action add \
  --title "{文章标题}" \
  --platform "{平台}" \
  --status "{draft|published|local_file}" \
  --file "{文件路径}" \
  --log-file "{EXTEND.md中的publish_log路径}"
```

日志格式（JSON）：

```json
{
  "entries": [
    {
      "id": "uuid",
      "title": "文章标题",
      "topic": "选题来源",
      "created_at": "2026-04-15T14:30:00+08:00",
      "platforms": {
        "wechat": { "status": "draft", "media_id": "xxx", "file": "wechat.md" },
        "toutiao": { "status": "draft", "file": "toutiao.md" },
        "feishu": { "status": "published", "node_token": "xxx", "file": "master.md" },
        "obsidian": { "status": "published", "file": "vault/path/to/article.md" },
        "zhihu": { "status": "local_file", "file": "zhihu.md" },
        "xiaohongshu": { "status": "local_file", "file": "xiaohongshu.md" },
        "moments": { "status": "local_file", "file": "moments.md" }
      }
    }
  ]
}
```

---

## 发布完成汇报

所有平台处理完毕后，向用户汇报结果：

```
汇报内容：
1. 文章标题
2. 各平台发布状态（草稿/已归档/本地文件）
3. 文件输出目录路径（用 file:// 链接）
4. 需要用户手动操作的事项（如去头条后台发布）
5. 如果是专题系列（场景2），提示下一篇的选题
```

用 present_files 展示关键输出文件。
