#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动从公开维护源抓取并生成分类 live.txt
目标分类：央视 / 卫视 / 凤凰 / 河南地方 / 上海地方 / 港澳台(精选)
"""

import re
import urllib.request
import ssl
from collections import defaultdict, OrderedDict
from datetime import datetime, timezone

SOURCES = [
    "https://live.zbds.top/tv/iptv4.txt",
    "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.txt",
    "https://cdn.jsdelivr.net/gh/vbskycn/iptv@master/tv/iptv4.txt",
]

# 简单超时与 UA
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; IPTV-Updater/1.0; +https://github.com/andywe0921-ops/iptv-live)"
}

def fetch(url, timeout=25):
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            data = r.read()
            # 尝试解码
            for enc in ("utf-8", "gbk", "gb2312"):
                try:
                    return data.decode(enc)
                except Exception:
                    continue
            return data.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[WARN] fetch failed {url}: {e}")
        return ""

def parse_txt(content):
    """解析 name,url 或 #genre# 格式，返回 list of (name, url)"""
    items = []
    if not content:
        return items
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ",#" in line or line.endswith(",#genre#"):
            continue
        if "," in line:
            parts = line.split(",", 1)
            if len(parts) == 2:
                name, url = parts[0].strip(), parts[1].strip()
                if name and url.startswith("http"):
                    items.append((name, url))
    return items

def classify(name):
    n = name.upper().replace(" ", "").replace("-", "")
    # 央视
    if re.search(r"CCTV|央视|CGTN|中央", name, re.I) or n.startswith("CCTV"):
        return "央视频道"
    # 凤凰
    if "凤凰" in name or "PHOENIX" in n or "FENG HUANG" in n:
        return "凤凰卫视"
    # 河南
    if "河南" in name or "梨园" in name or "中原" in name:
        return "河南地方"
    # 上海
    if "上海" in name or "东方卫视" in name or "第一财经" in name or "ICS" in n:
        return "上海地方"
    # 卫视（省级）
    if "卫视" in name:
        return "卫视频道"
    # 港澳台 精选（尽量官方或常见国内可尝试）
    if any(k in name for k in ["港台電視", "RTHK", "凤凰", "澳门莲花", "TVB", "有線", "Now新聞", "香港"]):
        return "港澳台"
    return None

def main():
    all_items = []
    for src in SOURCES:
        print(f"Fetching {src} ...")
        content = fetch(src)
        items = parse_txt(content)
        print(f"  -> {len(items)} items")
        all_items.extend(items)

    # 分类 + 去重（同名保留多个不同 URL，最多 3 个）
    groups = defaultdict(lambda: OrderedDict())  # name -> list of urls
    for name, url in all_items:
        cat = classify(name)
        if not cat:
            continue
        key = re.sub(r"\s+", "", name)
        if key not in groups[cat]:
            groups[cat][key] = {"display": name, "urls": []}
        urls = groups[cat][key]["urls"]
        if url not in urls and len(urls) < 3:
            urls.append(url)

    # 固定输出顺序
    order = ["央视频道", "卫视频道", "凤凰卫视", "河南地方", "上海地方", "港澳台"]

    lines = []
    lines.append(f"# 自动更新于 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("# 来源：公开维护列表聚合过滤，仅供学习测试")
    lines.append("")

    total = 0
    for cat in order:
        if cat not in groups or not groups[cat]:
            continue
        lines.append(f"{cat},#genre#")
        for info in groups[cat].values():
            for u in info["urls"]:
                lines.append(f"{info['display']},{u}")
                total += 1
        lines.append("")

    out = "\n".join(lines).strip() + "\n"
    with open("live.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote live.txt with {total} entries")
    return total

if __name__ == "__main__":
    main()
