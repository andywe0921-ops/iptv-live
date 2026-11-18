# IPTV 直播源（自动更新）

个人整理的干净分类直播源，适合 **影视仓 / TVBox / APTV** 等播放器直接订阅。

每天通过 **GitHub Actions** 自动从公开维护列表抓取、过滤并更新 `live.txt`。

## 订阅地址（推荐）

**国内加速（优先用这个）：**
```
https://cdn.jsdelivr.net/gh/andywe0921-ops/iptv-live@main/live.txt
```

**原始地址：**
```
https://raw.githubusercontent.com/andywe0921-ops/iptv-live/main/live.txt
```

## 分类

- 央视频道
- 卫视频道
- 凤凰卫视
- 河南地方
- 上海地方
- 港澳台（精选，尽量选国内可尝试的源）

## 影视仓添加方法

1. 打开影视仓 → 直播 → 设置 / 直播源管理
2. 添加直播源 → 粘贴上面的 jsDelivr 地址
3. 保存并刷新

## 自动更新说明

本仓库已配置 GitHub Actions：

- 每天 UTC 02:00（北京时间约 10:00）自动运行
- 从 `live.zbds.top` 等公开源抓取
- 过滤出央视 / 卫视 / 凤凰 / 河南 / 上海 / 港澳台相关频道
- 每个频道最多保留 3 个不同地址
- 有变化时自动提交 `live.txt`

### 如何启用 Actions（重要！）

1. 打开仓库：https://github.com/andywe0921-ops/iptv-live
2. 点击上方 **Actions** 标签页
3. 如果提示需要启用，点击绿色按钮 **I understand my workflows, go ahead and enable them**
4. 左侧找到 **Auto Update Live Sources**，点击 **Enable workflow**
5. 之后可以点 **Run workflow** 手动触发一次立即更新

## 说明

- 源全部来自公开网络，仅供学习测试，不保证永久有效。
- 港澳台源在大陆网络下不保证全部流畅。
- 建议同时订阅更全的自动更新源作为备份：
  - https://live.zbds.top/tv/iptv4.txt

仓库：https://github.com/andywe0921-ops/iptv-live
