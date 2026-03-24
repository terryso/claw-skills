# 统计分析

## 概述

统计命令提供频道表现、观众行为和直播质量的洞察数据。

## 概览统计

```bash
# 频道概览
npx polyv-live-cli@latest statistics overview -c 3151318

# 输出包含：
# 总观看次数: 15,420
# 独立观众数: 8,234
# 平均观看时长: 32:15
# 峰值并发: 1,245
# 总点赞数: 3,456
# 总评论数: 892
```

### JSON输出

```bash
npx polyv-live-cli@latest statistics overview -c 3151318 -o json
```

## 观看数据

按时间查看详细观看统计。

```bash
# 默认观看数据
npx polyv-live-cli@latest statistics viewdata -c 3151318

# 指定日期范围
npx polyv-live-cli@latest statistics viewdata \
  -c 3151318 \
  --start-date 2024-06-01 \
  --end-date 2024-06-30
```

### 观看数据选项

| 选项 | 说明 | 格式 |
|------|------|------|
| `--start-date` | 开始日期 | YYYY-MM-DD |
| `--end-date` | 结束日期 | YYYY-MM-DD |
| `--interval` | 数据分组 | hour/day/week |

## 汇总报告

```bash
# 频道汇总
npx polyv-live-cli@latest statistics summary -c 3151318

# 输出包含：
# 直播场次: 45
# 总时长: 67:30:00
# 平均时长: 01:30:00
# 最佳日期: 2024-06-15 (2,345 观众)
```

## 导出统计

### 导出为CSV

```bash
npx polyv-live-cli@latest statistics export \
  -c 3151318 \
  -f csv \
  -o channel-stats.csv

# 输出：
# ✅ 已导出到 channel-stats.csv
# 记录数: 1,234
```

### 导出为JSON

```bash
npx polyv-live-cli@latest statistics export \
  -c 3151318 \
  -f json \
  -o channel-stats.json
```

### 导出选项

| 选项 | 说明 | 可选值 |
|------|------|--------|
| `-f, --format` | 导出格式 | csv, json, xlsx |
| `-o, --output` | 输出文件路径 | - |
| `--start-date` | 开始日期 | YYYY-MM-DD |
| `--end-date` | 结束日期 | YYYY-MM-DD |

## 场次统计

获取特定直播场次的统计数据。

```bash
# 场次列表
npx polyv-live-cli@latest statistics sessions -c 3151318

# 特定场次
npx polyv-live-cli@latest statistics session -c 3151318 --sessionId sess001
```

## 观众分析

```bash
# 观众地域分布
npx polyv-live-cli@latest statistics viewers -c 3151318

# 输出包含：
# 热门地区: 北京(23%), 上海(18%), 广州(12%)
# 设备类型: 移动端(65%), 桌面端(35%)
# 热门浏览器: Chrome(45%), Safari(30%), 微信(15%)
```

## 互动指标

```bash
# 互动汇总
npx polyv-live-cli@latest statistics engagement -c 3151318

# 输出包含：
# 平均互动率: 78%
# 峰值互动率: 95% (00:32:15)
# 聊天消息: 1,234
# 点赞数: 3,456
# 分享数: 234
```

## 常用工作流程

### 生成周报

```bash
# 生成周报
npx polyv-live-cli@latest statistics export \
  -c 3151318 \
  -f csv \
  -o weekly-report.csv \
  --start-date 2024-06-10 \
  --end-date 2024-06-16

# 获取汇总
npx polyv-live-cli@latest statistics summary -c 3151318 -o json > summary.json
```

### 对比多个频道

```bash
# 导出多个频道的统计
for channel in 3151318 3151319 3151320; do
  npx polyv-live-cli@latest statistics overview -c $channel -o json > "channel-$channel.json"
done

# 对比分析
jq -s '.' channel-*.json > comparison.json
```

### 增长追踪

```bash
# 每日追踪脚本
#!/bin/bash
DATE=$(date +%Y-%m-%d)
npx polyv-live-cli@latest statistics overview -c 3151318 -o json | \
  jq --arg date "$DATE" '. + {date: $date}' >> daily-stats.jsonl
```

## 可用指标

| 指标 | 说明 |
|------|------|
| `totalViews` | 总观看次数 |
| `uniqueViewers` | 独立观众数 |
| `avgWatchTime` | 平均观看时长 |
| `peakConcurrent` | 峰值并发人数 |
| `totalLikes` | 总点赞数 |
| `totalComments` | 总评论数 |
| `totalShares` | 总分享数 |
| `engagementRate` | 互动率 |

## 故障排除

### "No data available"（无可用数据）

- 检查日期范围是否有效
- 确认频道已有直播场次
- 确保数据已处理完成（最多需要24小时）

### "Export failed"（导出失败）

- 检查输出路径的写入权限
- 确保有足够的磁盘空间
- 尝试其他导出格式

### "Date range too large"（日期范围过大）

- 最大范围通常为90天
- 分成较小的日期范围
- 使用 --interval 聚合数据
