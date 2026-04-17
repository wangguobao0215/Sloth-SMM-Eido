# 品牌素材目录

将您的公众号品牌题图和底图放在此目录中，然后在 EXTEND.md 中配置路径。

## 推荐规格

- 题图（header）：宽度 900-1080px，高度不限，JPEG/PNG 格式
- 底图（footer）：宽度 900-1080px，高度不限，JPEG/PNG 格式

## 配置方式

在 EXTEND.md 中设置：

```yaml
wechat_ads:
  header_image: "{skill_dir}/assets/your-header.jpeg"
  footer_image: "{skill_dir}/assets/your-footer.jpeg"
```

如不需要品牌图，留空即可。
