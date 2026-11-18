# IPTV 直播源

个人整理的干净分类直播源，适合 **影视仓 / TVBox / APTV** 等播放器直接订阅。

## 订阅地址（推荐）

**TXT 格式（影视仓友好）：**
```
https://raw.githubusercontent.com/andywe0921-ops/iptv-live/main/live.txt
```

**国内加速（推荐）：**
```
https://cdn.jsdelivr.net/gh/andywe0921-ops/iptv-live@main/live.txt
```
或
```
https://ghproxy.com/https://raw.githubusercontent.com/andywe0921-ops/iptv-live/main/live.txt
```

## 分类

- 央视频道（CCTV1-17 + CGTN 等）
- 卫视频道（主流省级卫视）
- 凤凰卫视（中文台、资讯台）
- 河南地方台
- 上海地方台
- 港澳台（已尽量选择国内网络可尝试播放的源）

## 影视仓添加方法

1. 打开影视仓 → 直播 → 设置 / 直播源管理
2. 添加直播源 → 粘贴上面的订阅地址
3. 保存并刷新列表

## 说明与限制

- 源来自公开网络，会失效，请定期刷新。
- 港澳台源在大陆网络下**不保证**全部流畅，已尽量筛选免代理可播的；真正稳定的港台源多数需要特定环境。
- 凤凰卫视已加入常见国内可用地址。
- 更推荐同时订阅自动更新的公开源作为备份：
  - https://live.zbds.top/tv/iptv4.txt
  - https://live.zbds.top/tv/iptv4.m3u

## 关于自动更新

完整的“某个源失效后自动抓取并替换新源”需要持续运行的验证服务器 + 多源爬虫，成本较高。

本仓库可后续添加 GitHub Actions 定期从公开维护列表同步更新。当前请手动或订阅上面的自动更新源。

仓库地址：https://github.com/andywe0921-ops/iptv-live
