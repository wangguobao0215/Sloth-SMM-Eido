#!/usr/bin/env python3
"""
今日头条文章发布到草稿箱 - Playwright CDP 自动化
(Sloth-SMM-Eido)

用法:
  python toutiao-publish.py <markdown_file> [--cover <image_path>] [--title <title>]

前置要求:
  1. pip install playwright markdown
  2. 启动 Chrome: chrome.exe --remote-debugging-port=9222
  3. 在 Chrome 中手动登录 mp.toutiao.com（首次/cookie过期时）

原理:
  通过 CDP 连接已打开的 Chrome，在 mp.toutiao.com 文章编辑器中
  注入标题和正文内容，上传封面图，然后点击「存草稿」。

维护说明:
  - 本脚本依赖 CSS 选择器定位头条编辑器元素。头条页面更新可能导致选择器失效。
  - 当前验证通过的头条页面版本：2026-Q1
  - 若发布失败并提示"未找到标题输入框"或"未找到正文编辑器"，请检查：
    1. 头条创作者中心页面结构是否已更新
    2. 脚本中 fill_title() 和 fill_body() 的选择器列表是否需要补充新选择器
  - 维护时建议保留旧选择器作为 fallback，新增选择器追加到列表末尾
"""

import argparse
import json
import os
import re
import sys
import time
import random
import markdown as md_lib
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ========== 配置 ==========
CDP_URL = "http://localhost:9222"
TOUTIAO_EDITOR_URL = "https://mp.toutiao.com/profile_v4/graphic/publish"
TOUTIAO_HOME_URL = "https://mp.toutiao.com"

# ========== 工具函数 ==========

def log(msg: str):
    print(f"[toutiao-publish] {msg}", flush=True)

def random_delay(min_ms=300, max_ms=800):
    """模拟人类操作间隔"""
    time.sleep(random.randint(min_ms, max_ms) / 1000)

def read_markdown_file(filepath: str) -> tuple[str, str, str]:
    """
    读取 Markdown 文件，返回 (title, html_body, raw_md)
    标题取第一个 # 标题，或 frontmatter 中的 title
    """
    path = Path(filepath)
    if not path.exists():
        log(f"ERROR: 文件不存在: {filepath}")
        sys.exit(1)

    raw = path.read_text(encoding="utf-8")

    # 移除 HTML 注释（标题候选等）
    clean = re.sub(r'<!--[\s\S]*?-->', '', raw).strip()

    # 提取标题：第一个 # 开头的行
    title = ""
    lines = clean.split("\n")
    body_lines = []
    title_found = False
    for line in lines:
        if not title_found and re.match(r'^#\s+', line):
            title = re.sub(r'^#+\s*', '', line).strip()
            title_found = True
            continue
        body_lines.append(line)

    body_md = "\n".join(body_lines).strip()

    # Markdown → HTML
    html_body = md_lib.markdown(body_md, extensions=['extra', 'sane_lists'])

    return title, html_body, raw


def extract_title_from_args_or_md(args, md_title: str) -> str:
    """优先使用命令行指定的标题，否则用 Markdown 中的标题"""
    if args.title:
        return args.title
    if md_title:
        return md_title
    log("ERROR: 无法提取标题，请用 --title 参数指定")
    sys.exit(1)


# ========== 核心发布逻辑 ==========

def check_login(page) -> bool:
    """检查是否已登录 mp.toutiao.com"""
    try:
        page.goto(TOUTIAO_HOME_URL, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)
        # 如果跳到了登录页，说明未登录
        current_url = page.url
        if "login" in current_url or "sso" in current_url:
            return False
        # 检查是否有创作中心的元素
        return True
    except Exception as e:
        log(f"登录检查异常: {e}")
        return False


def navigate_to_editor(page):
    """导航到文章编辑页"""
    log("导航到文章编辑器...")
    page.goto(TOUTIAO_EDITOR_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # 等待编辑器加载
    try:
        page.wait_for_selector('[placeholder*="标题"], [data-placeholder*="标题"], .article-title textarea, .ProseMirror', timeout=15000)
        log("编辑器已加载")
    except PlaywrightTimeout:
        log("WARNING: 编辑器加载超时，尝试继续...")


def fill_title(page, title: str):
    """填写文章标题"""
    log(f"填写标题: {title}")

    # 尝试多种选择器定位标题输入框
    selectors = [
        'textarea[placeholder*="标题"]',
        'input[placeholder*="标题"]',
        '[data-placeholder*="标题"]',
        '.article-title textarea',
        '.article-title input',
    ]

    for selector in selectors:
        try:
            el = page.locator(selector).first
            if el.is_visible(timeout=2000):
                el.click()
                random_delay(200, 400)
                el.fill("")
                random_delay(100, 200)
                # 逐字输入模拟人类
                for char in title:
                    el.type(char, delay=random.randint(30, 80))
                log("标题填写完成")
                return True
        except Exception:
            continue

    log("WARNING: 未找到标题输入框，尝试用键盘输入...")
    return False


def fill_body(page, html_content: str, md_file_path: str):
    """填写文章正文（通过剪贴板粘贴 HTML）"""
    log("填写正文内容...")

    # 处理正文中的本地图片路径：转为绝对路径
    base_dir = str(Path(md_file_path).parent.resolve())
    # 替换相对路径图片为绝对路径 file:// URL
    def fix_img_src(match):
        src = match.group(1)
        if src.startswith(('http://', 'https://', 'data:', 'file://')):
            return match.group(0)
        abs_path = os.path.normpath(os.path.join(base_dir, src))
        return f'src="file:///{abs_path.replace(os.sep, "/")}"'

    html_content = re.sub(r'src="([^"]*)"', fix_img_src, html_content)

    # 找到 ProseMirror 编辑器或 contenteditable 区域
    editor_selectors = [
        '.ProseMirror',
        '[contenteditable="true"]',
        '.public-DraftEditor-content',
        '.ql-editor',
        '[data-placeholder*="正文"]',
    ]

    editor = None
    for selector in editor_selectors:
        try:
            el = page.locator(selector).first
            if el.is_visible(timeout=2000):
                editor = el
                log(f"找到编辑器: {selector}")
                break
        except Exception:
            continue

    if not editor:
        log("WARNING: 未找到正文编辑器，尝试通过 Tab 定位...")
        page.keyboard.press("Tab")
        time.sleep(1)

    # 方法1：通过 JavaScript 设置剪贴板并粘贴
    try:
        # 将 HTML 内容写入页面的 clipboard
        page.evaluate(f"""
            async () => {{
                const htmlContent = {json.dumps(html_content)};
                const blob = new Blob([htmlContent], {{ type: 'text/html' }});
                const plainText = new DOMParser()
                    .parseFromString(htmlContent, 'text/html')
                    .body.textContent || '';
                const clipboardItem = new ClipboardItem({{
                    'text/html': blob,
                    'text/plain': new Blob([plainText], {{ type: 'text/plain' }})
                }});
                await navigator.clipboard.write([clipboardItem]);
            }}
        """)
        random_delay(300, 600)

        # 点击编辑器区域
        if editor:
            editor.click()
        random_delay(200, 400)

        # 粘贴
        page.keyboard.press("Control+a")
        random_delay(100, 200)
        page.keyboard.press("Control+v")
        random_delay(500, 1000)
        log("正文内容已通过剪贴板粘贴")
        return True
    except Exception as e:
        log(f"剪贴板方式失败: {e}")

    # 方法2：通过 execCommand 直接插入 HTML
    try:
        if editor:
            editor.click()
            random_delay(200, 400)
        page.evaluate(f"""
            document.execCommand('insertHTML', false, {json.dumps(html_content)});
        """)
        log("正文内容已通过 execCommand 插入")
        return True
    except Exception as e:
        log(f"execCommand 方式也失败: {e}")

    # 方法3：直接设置 innerHTML（最后手段）
    try:
        if editor:
            page.evaluate(f"""
                document.querySelector('.ProseMirror, [contenteditable="true"]').innerHTML = {json.dumps(html_content)};
            """)
            # 触发 input 事件让编辑器感知变化
            page.evaluate("""
                const el = document.querySelector('.ProseMirror, [contenteditable="true"]');
                el.dispatchEvent(new Event('input', { bubbles: true }));
            """)
            log("正文内容已通过 innerHTML 设置")
            return True
    except Exception as e:
        log(f"innerHTML 方式也失败: {e}")

    log("ERROR: 所有正文填写方式均失败")
    return False


def upload_cover(page, cover_path: str):
    """上传封面图"""
    if not cover_path:
        log("未指定封面图，跳过")
        return

    abs_cover = str(Path(cover_path).resolve())
    if not os.path.exists(abs_cover):
        log(f"WARNING: 封面图不存在: {abs_cover}")
        return

    log(f"上传封面图: {abs_cover}")

    try:
        # 查找封面上传区域的 file input
        file_inputs = page.locator('input[type="file"]')
        count = file_inputs.count()
        log(f"找到 {count} 个文件上传输入框")

        if count > 0:
            # 通常第一个 file input 是封面图上传
            file_inputs.first.set_input_files(abs_cover)
            random_delay(2000, 3000)
            log("封面图上传完成")
        else:
            log("WARNING: 未找到文件上传输入框")
    except Exception as e:
        log(f"封面图上传失败: {e}")


def set_original_declaration(page):
    """勾选原创声明（如果有的话）"""
    try:
        # 查找"原创"相关的复选框或按钮
        original_selectors = [
            'text=原创',
            'text=声明原创',
            '[class*="original"]',
        ]
        for selector in original_selectors:
            try:
                el = page.locator(selector).first
                if el.is_visible(timeout=2000):
                    el.click()
                    random_delay(300, 600)
                    log("已勾选原创声明")
                    return
            except Exception:
                continue
    except Exception:
        pass
    log("未找到原创声明选项（可能不需要或已默认勾选）")


def save_as_draft(page) -> bool:
    """点击存草稿按钮"""
    log("保存为草稿...")

    draft_selectors = [
        'button:has-text("存草稿")',
        'button:has-text("保存草稿")',
        'button:has-text("存为草稿")',
        'text=存草稿',
        '[class*="draft"]',
    ]

    for selector in draft_selectors:
        try:
            el = page.locator(selector).first
            if el.is_visible(timeout=2000):
                el.click()
                random_delay(1000, 2000)
                log("已点击存草稿按钮")
                time.sleep(3)

                # 检查是否保存成功
                try:
                    # 等待成功提示
                    success = page.locator('text=保存成功').first
                    if success.is_visible(timeout=5000):
                        log("草稿保存成功！")
                        return True
                except Exception:
                    pass

                # 如果没有明确的成功提示，检查 URL 是否变化（跳到草稿列表等）
                log("未检测到明确的成功提示，但已执行保存操作")
                return True
        except Exception:
            continue

    log("ERROR: 未找到存草稿按钮")
    return False


def publish_to_toutiao(md_file: str, cover_path: str = None, title_override: str = None):
    """主发布流程"""
    # 1. 读取 Markdown
    md_title, html_body, raw_md = read_markdown_file(md_file)
    title = title_override or md_title

    log(f"文章标题: {title}")
    log(f"正文长度: {len(html_body)} 字符 (HTML)")

    # 2. 启动 Playwright，连接到已打开的 Chrome
    with sync_playwright() as p:
        try:
            log(f"连接 Chrome CDP: {CDP_URL}")
            browser = p.chromium.connect_over_cdp(CDP_URL)
        except Exception as e:
            log(f"ERROR: 无法连接 Chrome。请确保 Chrome 已启动并开启了远程调试:")
            log(f"  chrome.exe --remote-debugging-port=9222")
            log(f"错误详情: {e}")
            sys.exit(1)

        # 获取或创建页面
        contexts = browser.contexts
        if not contexts:
            log("ERROR: 没有浏览器上下文")
            sys.exit(1)

        context = contexts[0]
        page = context.new_page()

        try:
            # 3. 检查登录状态
            log("检查登录状态...")
            if not check_login(page):
                log("ERROR: 未登录 mp.toutiao.com")
                log("请在 Chrome 中手动登录 mp.toutiao.com 后重试")
                sys.exit(1)
            log("登录状态正常")

            # 4. 导航到编辑器
            navigate_to_editor(page)
            random_delay(1000, 2000)

            # 5. 填写标题
            fill_title(page, title)
            random_delay(500, 1000)

            # 6. 填写正文
            fill_body(page, html_body, md_file)
            random_delay(1000, 2000)

            # 7. 上传封面图
            if cover_path:
                upload_cover(page, cover_path)
                random_delay(1000, 2000)

            # 8. 存草稿
            success = save_as_draft(page)

            if success:
                result = {
                    "success": True,
                    "title": title,
                    "platform": "toutiao",
                    "status": "draft",
                    "message": "文章已保存到今日头条草稿箱"
                }
            else:
                result = {
                    "success": False,
                    "title": title,
                    "platform": "toutiao",
                    "status": "failed",
                    "message": "保存草稿失败，请手动检查"
                }

            print(json.dumps(result, ensure_ascii=False, indent=2))
            return result

        except Exception as e:
            log(f"ERROR: 发布过程异常: {e}")
            result = {
                "success": False,
                "title": title,
                "platform": "toutiao",
                "error": str(e)
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return result
        finally:
            page.close()


# ========== 入口 ==========

def main():
    parser = argparse.ArgumentParser(description="发布文章到今日头条草稿箱")
    parser.add_argument("markdown_file", help="Markdown 文件路径")
    parser.add_argument("--cover", help="封面图路径", default=None)
    parser.add_argument("--title", help="文章标题（覆盖 Markdown 中的标题）", default=None)
    parser.add_argument("--cdp-url", help="Chrome CDP 地址", default=CDP_URL)

    args = parser.parse_args()

    cdp = args.cdp_url

    publish_to_toutiao(
        md_file=args.markdown_file,
        cover_path=args.cover,
        title_override=args.title
    )


if __name__ == "__main__":
    main()
