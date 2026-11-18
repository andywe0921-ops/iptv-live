#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动从公开维护源抓取并生成分类 live.txt
优先保留用户反馈流畅的 CCTV 节点，并尽量补全卫视
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

# 用户反馈较流畅的优先源（放在最前面）
PREFERRED = [
    ("CCTV1综合", "http://123.160.173.129:85/tsfile/live/0001_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV1综合", "http://gmxw.7766.org:808/hls/89/index.m3u8"),
    ("CCTV2财经", "http://123.160.173.129:85/tsfile/live/0002_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV3", "http://gmxw.7766.org:808/hls/91/index.m3u8"),
    ("CCTV4中文国际", "http://123.160.173.129:85/tsfile/live/0004_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV5", "http://gmxw.7766.org:808/hls/93/index.m3u8"),
    ("CCTV6电影", "http://123.160.173.129:85/tsfile/live/0006_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV7国防军事", "http://123.160.173.129:85/tsfile/live/0007_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV8", "http://gmxw.7766.org:808/hls/96/index.m3u8"),
    ("CCTV9纪录", "http://123.160.173.129:85/tsfile/live/0009_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV10科教", "http://123.160.173.129:85/tsfile/live/0010_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV11戏曲", "http://123.160.173.129:85/tsfile/live/0011_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV14少儿", "http://123.160.173.129:85/tsfile/live/0014_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("CCTV15", "http://gmxw.7766.org:808/hls/102/index.m3u8"),
    ("CCTV16", "http://gmxw.7766.org:808/hls/169/index.m3u8"),
    ("北京卫视", "http://123.160.173.129:85/tsfile/live/0122_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("广东卫视", "http://123.160.173.129:85/tsfile/live/0125_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("深圳卫视", "http://123.160.173.129:85/tsfile/live/0126_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("河南卫视", "http://123.160.173.129:85/tsfile/live/0139_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("凤凰中文", "http://123.160.173.129:85/tsfile/live/1020_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("凤凰中文", "http://221.7.175.154:8445/tsfile/live/1020_1.m3u8?key=txiptv&playlive=1&authid=0"),
    ("凤凰资讯", "http://221.7.175.154:8445/tsfile/live/1021_1.m3u8?key=txiptv&playlive=1&authid=0"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; IPTV-Updater/1.0; +https://github.com/andywe0921-ops/iptv-live)"
}

def fetch(url, timeout=25):
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            data = r.read()
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
                if name and url.startswith("http") and "mp4" not in url.lower():
                    items.append((name, url))
    return items

def classify(name):
    n = name.upper().replace(" ", "").replace("-", "")
    if re.search(r"CCTV|央视|CGTN|中央", name, re.I) or n.startswith("CCTV"):
        return "央视频道"
    if "凤凰" in name or "PHOENIX" in n:
        return "凤凰卫视"
    if "河南" in name or "梨园" in name or "中原" in name:
        return "河南地方"
    if "上海" in name or "东方卫视" in name or "第一财经" in name:
        return "上海地方"
    if "卫视" in name:
        return "卫视频道"
    if any(k in name for k in ["港台電視", "RTHK", "澳门莲花", "TVB", "有線", "Now新聞", "香港"]):
        return "港澳台"
    return None

def main():
    all_items = list(PREFERRED)  # 优先源放最前
    for src in SOURCES:
        print(f"Fetching {src} ...")
        content = fetch(src)
        items = parse_txt(content)
        print(f"  -> {len(items)} items")
        all_items.extend(items)

    groups = defaultdict(lambda: OrderedDict())
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

    order = ["央视频道", "卫视频道", "凤凰卫视", "河南地方", "上海地方", "港澳台"]

    lines = []
    lines.append(f"# 自动更新于 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("# 来源：公开维护列表 + 优先流畅节点，仅供学习测试")
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
