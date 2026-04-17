#!/usr/bin/env python3
"""
Sloth-SMM-Eido 发布日志管理脚本

用法:
  python publish-log.py --action add --title "文章标题" --platform "wechat" --status "draft" --file "path/to/file.md"
  python publish-log.py --action add --title "文章标题" --platform "feishu" --status "published" --node-token "xxx"
  python publish-log.py --action list
  python publish-log.py --action list --platform "wechat"
"""

import json
import os
import sys
import uuid
import argparse
from datetime import datetime, timezone, timedelta


def get_log_path(custom_path=None):
    """获取日志文件路径"""
    if custom_path:
        return custom_path
    return os.path.join(os.getcwd(), "publish-log.json")


def load_log(log_path):
    """加载日志文件"""
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"entries": []}


def save_log(log_path, data):
    """保存日志文件"""
    os.makedirs(os.path.dirname(log_path) if os.path.dirname(log_path) else ".", exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_entry(log_data, title, platform, status, file_path=None,
              media_id=None, node_token=None, topic=None):
    """添加一条发布记录"""
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz).isoformat()

    # 查找是否已有同标题的条目
    existing = None
    for entry in log_data["entries"]:
        if entry["title"] == title:
            existing = entry
            break

    platform_record = {
        "status": status,
        "file": file_path or "",
        "published_at": now
    }
    if media_id:
        platform_record["media_id"] = media_id
    if node_token:
        platform_record["node_token"] = node_token

    if existing:
        existing["platforms"][platform] = platform_record
        existing["updated_at"] = now
        print(f"Updated: {title} -> {platform}: {status}")
    else:
        entry = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "topic": topic or "",
            "created_at": now,
            "updated_at": now,
            "platforms": {
                platform: platform_record
            }
        }
        log_data["entries"].append(entry)
        print(f"Added: {title} -> {platform}: {status}")

    return log_data


def list_entries(log_data, platform_filter=None):
    """列出发布记录"""
    entries = log_data.get("entries", [])
    if not entries:
        print("No publish records found.")
        return

    for entry in entries:
        print(f"\n{'='*60}")
        print(f"Title: {entry['title']}")
        print(f"Topic: {entry.get('topic', 'N/A')}")
        print(f"Created: {entry['created_at']}")
        print(f"Platforms:")
        for pf, info in entry.get("platforms", {}).items():
            if platform_filter and pf != platform_filter:
                continue
            status_label = {"draft": "[DRAFT]", "published": "[PUBLISHED]", "local_file": "[LOCAL]"}.get(info["status"], "[?]")
            print(f"  {status_label} {pf}: {info['status']} | {info.get('file', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(description="Sloth-SMM-Eido Publish Log Manager")
    parser.add_argument("--action", required=True, choices=["add", "list"],
                        help="Action to perform")
    parser.add_argument("--title", help="Article title")
    parser.add_argument("--platform", help="Platform name (wechat/feishu/toutiao/zhihu/xiaohongshu)")
    parser.add_argument("--status", choices=["draft", "published", "local_file"],
                        help="Publish status")
    parser.add_argument("--file", help="File path")
    parser.add_argument("--media-id", help="WeChat media ID")
    parser.add_argument("--node-token", help="Feishu node token")
    parser.add_argument("--topic", help="Topic/source")
    parser.add_argument("--log-file", help="Custom log file path")

    args = parser.parse_args()
    log_path = get_log_path(args.log_file)

    if args.action == "add":
        if not args.title or not args.platform or not args.status:
            print("Error: --title, --platform, and --status are required for 'add' action")
            sys.exit(1)
        log_data = load_log(log_path)
        log_data = add_entry(
            log_data, args.title, args.platform, args.status,
            file_path=args.file, media_id=args.media_id,
            node_token=args.node_token, topic=args.topic
        )
        save_log(log_path, log_data)

    elif args.action == "list":
        log_data = load_log(log_path)
        list_entries(log_data, platform_filter=args.platform)


if __name__ == "__main__":
    main()
