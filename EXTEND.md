# Sloth-SMM-Eido 用户配置（示例模板）
# 首次使用时请根据自己的需求修改以下配置

# ===== 内容领域 =====
# 影响热点抓取源和选题方向
# 可选: 科技/AI, 个人成长, 职场效率, 商业/财经, 生活方式, 混合
domains:
  - 科技/AI
  - 个人成长

# ===== 默认写作风格 =====
# auto: 根据选题和平台自动匹配（推荐）
# deep: 深度干货型 | story: 故事情感型 | sharp: 观点犀利型 | light: 轻松科普型
default_style: auto

# ===== 新闻源偏好 =====
news_sources:
  - 36kr
  - weibo
  - hackernews
  - wallstreetcn

news_keywords: ""

# ===== 平台开关 =====
platforms:
  wechat: true
  toutiao: true
  zhihu: true
  xiaohongshu: true
  moments: true

# ===== 微信公众号配置 =====
wechat:
  method: api          # api 或 browser
  theme: grace         # default / grace / simple / modern
  color: blue          # blue/green/vermilion/yellow/purple 等
  author: ""           # 文章作者名，留空则不显示
  account: ""          # 多账号时指定，留空用默认

# ===== 公众号品牌图（题图 & 底图） =====
# 在公众号文章正文的首尾自动插入品牌图
# 将您的品牌题图和底图放入 assets/ 目录，然后在这里配置路径
# 留空表示不插入品牌图
wechat_ads:
  header_image: "/Users/wangguobao/Desktop/Sloth-Role-Eido/Sloth-SMM-Eido/assets/slothk-header.png"
  footer_image: "/Users/wangguobao/Desktop/Sloth-Role-Eido/Sloth-SMM-Eido/assets/slothk-footer.png"

# ===== 今日头条配置 =====
toutiao:
  enabled: true
  cdp_url: "http://localhost:9222"

# ===== 朋友圈配置 =====
moments:
  enabled: true

# ===== 飞书知识库配置 =====
feishu:
  space_id: ""
  parent_node: ""
  identity: user
  enabled: false       # 默认关闭，需要时开启并配置 space_id

feishu_platforms:
  wechat:
    space_id: ""
    parent_node: ""
  toutiao:
    space_id: ""
    parent_node: ""
  zhihu:
    space_id: ""
    parent_node: ""
  xiaohongshu:
    space_id: ""
    parent_node: ""

# ===== 文件输出配置 =====
output:
  base_dir: ""
  folder_pattern: "{date}_{slug}"

# ===== 配图配置 =====
illustration:
  enabled: true
  style: ""
  xhs_preset: knowledge-card

publish_log: publish-log.json

# ===== Obsidian 本地知识库归档 =====
obsidian:
  enabled: false       # 默认关闭，需要时开启并配置 vault_path
  vault_path: ""       # 您的 Obsidian vault 根目录路径
  folder: "自媒体文章"
  copy_images: true
  wikilinks: false
  frontmatter_extras: {}

# ===== Windows 兼容 =====
# set PYTHONIOENCODING=utf-8
