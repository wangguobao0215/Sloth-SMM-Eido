# 模块D：排版引擎 (Format Engine)

## 概述

将平台适配后的文章进行排版和配图处理，使其在各平台上呈现最佳视觉效果。

## 排版流程

```
读取各平台适配版本
→ 公众号: 调用 baoyu-post-to-wechat 做 Markdown→微信HTML 转换
→ 长文平台(公众号/头条/知乎): 调用 baoyu-article-illustrator 生成配图
→ 小红书: 调用 baoyu-xhs-images 生成图卡
→ 输出排版后文件和图片
```

## 公众号排版

公众号排版依赖 baoyu-post-to-wechat 的内置主题系统，不需要额外排版。

读取 EXTEND.md 中的 wechat 配置（theme, color），在发布阶段直接传参即可。

排版注意事项：
- Markdown 中的外部链接会被自动转为底部引用（skill内置功能）
- 图片使用相对路径指向 images/ 目录
- 如果需要自定义样式，在 wechat.md 的 frontmatter 中指定 theme 和 color 即可覆盖默认

### 公众号题图 & 底图（品牌图）

读取 EXTEND.md 中的 `wechat_ads` 配置，如果配置了 header_image 或 footer_image，在 wechat.md 正文内容中自动插入。

**插入时机**：在所有内容改写和配图插入完成之后、交给 baoyu-post-to-wechat 发布之前。

**插入规则**：

```
1. 读取 EXTEND.md → wechat_ads.header_image 和 wechat_ads.footer_image
2. 如果 header_image 非空：
   - 将该图片复制到文章的 images/ 目录（保留原文件名）
   - 在 wechat.md 正文最前面（frontmatter 之后、第一行内容之前）插入：
     ![题图](images/{header_image文件名})
   - 空一行后才接正文
3. 如果 footer_image 非空：
   - 将该图片复制到文章的 images/ 目录（保留原文件名）
   - 在 wechat.md 正文最后面追加空行，然后插入：
     ![底图](images/{footer_image文件名})
4. 如果两个都为空，则跳过此步骤，不影响原有流程
```

**注意**：
- 题图和底图只插入公众号版本（wechat.md），不影响头条/知乎/小红书版本
- baoyu-post-to-wechat 在发布时会自动将 Markdown 图片上传到微信 CDN，无需额外处理
- 建议品牌图尺寸：题图宽度 900px-1080px，底图同理，高度不限

## 长文配图（公众号/头条/知乎）— 强制步骤

⚠️ **此步骤为必须执行步骤，不可跳过。** 每篇文章在生成平台版本后、发布之前，必须调用 baoyu-article-illustrator 生成正文配图。

**正文配图 ≠ 品牌图**：
- 品牌图只用于文首题图和文末底图的固定位置
- 正文配图是根据文章内容生成的内容插图，插入在正文段落之间
- **严禁用品牌图替代正文配图，严禁跳过此步骤**

使用 baoyu-article-illustrator 为文章自动生成配图。

### 调用方式

```
1. 将母版文章(master.md)传给 baoyu-article-illustrator
2. 使用参数：
   - --preset: 根据文章风格选择
     deep → edu-visual 或 blueprint
     story → warm-illustration 或 watercolor
     sharp → editorial 或 poster
     light → minimal-flat 或 notion
   - 如果 EXTEND.md 配置了 illustration.style，优先使用
3. illustrator 会分析文章结构，自动确定：
   - 需要几张配图
   - 每张图放在文章的什么位置
   - 每张图的内容主题
4. 生成的图片保存到 images/ 目录
```

### 图片插入

配图生成后，将图片路径插入到各平台版本的对应位置：

```markdown
![图片描述](images/01-infographic-xxx.png)
```

注意：
- 公众号版本的图片会在发布时自动上传到微信服务器
- 头条和知乎版本的图片保持本地路径，用户手动发布时需要上传
- 每篇文章配图数量建议：deep=3-5张, story=2-3张, sharp=2-3张, light=3-4张
- **正文配图插入位置**：应插在小标题后、段落之间等视觉节奏需要"呼吸"的位置
- **正文配图不要插在品牌题图/底图的位置**——品牌图和正文配图是完全独立的两套图片

## 小红书图卡

小红书的"排版"本质是生成一组视觉图卡，文字只是辅助。

### 调用方式

```
1. 读取小红书适配版本(xiaohongshu.md)
2. 调用 baoyu-xhs-images：
   - 输入: xiaohongshu.md 的内容
   - 参数: --yes --preset {EXTEND.md中的xhs_preset，默认knowledge-card}
   - 如果母版风格是 story → 使用 story-driven 大纲策略
   - 如果母版风格是 deep/sharp → 使用 information-dense 大纲策略
   - 如果母版风格是 light → 使用 visual-first 大纲策略
3. 输出到 xhs-images/ 目录
```

### 图卡优化

baoyu-xhs-images 会自动处理：
- 封面图设计（第1张，最重要）
- 内容拆分为多张卡片（通常4-8张）
- 结尾图（引导关注）
- 图片间的视觉一致性（Reference Image Chain）

## 今日头条排版

头条文章以 Markdown 形式输出，排版要点由平台适配器在内容改写时已处理：
- 短段落
- 高频小标题
- 图片位置标注

额外处理：
- 在每张配图后添加图片描述（头条支持图片描述，有助于推荐）
- 确保首图放在文章开头（头条封面默认取首图）

## 知乎排版

知乎文章以 Markdown 形式输出，排版要点：
- 引用块 `>` 用于专家观点和数据来源
- 代码块用于技术内容（如果有）
- 表格用于对比数据
- 分割线 `---` 用于大段落分隔
- 图片居中，添加图注

## 输出检查

排版完成后，检查每个平台版本：

```
□ 公众号: wechat.md 中图片路径正确，frontmatter 完整
□ 头条: toutiao.md 首图存在，图片描述完整
□ 知乎: zhihu.md 引用格式正确，图片有图注
□ 小红书: xhs-images/ 目录中图卡数量正确(至少4张)
□ 所有图片文件确实存在于 images/ 和 xhs-images/ 目录
```
