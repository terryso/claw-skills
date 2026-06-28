---
name: akshare-stock
slug: akshare-stock-cn
displayName: A股量化数据分析
version: 1.1.0
summary: 基于 AkShare 获取A股实时行情、历史K线、财务数据、资金流向、龙虎榜、融资融券等数据，封装为可执行 CLI 脚本
license: MIT
description: A股量化数据分析工具，基于AkShare库获取A股行情、财务数据、板块信息等。提供可执行 CLI 脚本，内置重试机制和错误处理。用于回答关于A股股票查询、行情数据、财务分析、选股等问题。
allowed-tools: Bash(python3:*), Bash(pip3:*)
---

# A股量化数据分析（AkShare）

基于 AkShare 封装的可执行 CLI 工具，内置重试机制、错误处理和 JSON/表格双格式输出。

## 环境准备

```bash
pip install akshare
```

## 使用方式

所有查询通过 CLI 脚本完成，`SKILL_DIR` 为本 SKILL.md 所在目录：

```bash
python3 SKILL_DIR/scripts/akshare_cli.py <子命令> [参数]
```

默认输出 JSON，加 `--format table` 输出表格。

### 实时行情

```bash
# 全市场实时行情
python3 SKILL_DIR/scripts/akshare_cli.py spot

# 指定板块
python3 SKILL_DIR/scripts/akshare_cli.py spot --board 北证A股
```

### 历史K线

```bash
# 日K线（默认近一年，前复权）
python3 SKILL_DIR/scripts/akshare_cli.py kline 000001

# 周K线 + 自定义日期范围
python3 SKILL_DIR/scripts/akshare_cli.py kline 000001 --period weekly --start 20240101 --end 20241231
```

### 财务数据

```bash
# 财务报表摘要
python3 SKILL_DIR/scripts/akshare_cli.py finance 000001

# 主要财务指标
python3 SKILL_DIR/scripts/akshare_cli.py indicator 000001
```

### 板块/行业分析

```bash
# 行业板块列表
python3 SKILL_DIR/scripts/akshare_cli.py board

# 概念板块列表
python3 SKILL_DIR/scripts/akshare_cli.py board --concept

# 指定板块内个股
python3 SKILL_DIR/scripts/akshare_cli.py board --cons 半导体
```

### 资金流向

```bash
# 个股资金流向（自动识别沪深市场）
python3 SKILL_DIR/scripts/akshare_cli.py fund 000001
```

### 龙虎榜

```bash
# 指定日期龙虎榜
python3 SKILL_DIR/scripts/akshare_cli.py lhb --date 20240930
```

### 新股/IPO

```bash
# 新股申购
python3 SKILL_DIR/scripts/akshare_cli.py ipo

# 待上市新股
python3 SKILL_DIR/scripts/akshare_cli.py ipo --upcoming
```

### 融资融券

```bash
# 融资融券数据
python3 SKILL_DIR/scripts/akshare_cli.py rzrq 600000
```

## 常用股票代码

| 股票 | 代码 |
|------|------|
| 平安银行 | 000001 |
| 贵州茅台 | 600519 |
| 宁德时代 | 300750 |
| 比亚迪 | 002594 |
| 招商银行 | 600036 |

## 脚本特性

- **内置重试机制：** 网络请求自动重试 2 次，指数退避
- **错误处理：** 异常返回 JSON `{"error": "..."}`，exit code=1
- **NaN 安全：** 自动处理 pandas NaN 值，避免 JSON 序列化失败
- **市场自动识别：** 根据股票代码前缀自动判断沪/深市场
- **双格式输出：** JSON（默认，适合 agent 解析）或 table（适合人类阅读）

## 备选方案: Baostock

AkShare 安装失败时可用 baostock（更轻量）：

```python
import baostock as bs

lg = bs.login()
rs = bs.query_history_k_data_plus('sh.600519',
    'date,code,open,high,low,close,volume',
    start_date='20250101', end_date='20251231')

data_list = []
while rs.next():
    data_list.append(rs.get_row_data())

bs.logout()
```

## 注意事项

1. 数据仅供学术研究，不构成投资建议
2. AkShare 接口依赖网络抓取，可能因目标网站变动而失效
3. CLI 脚本已内置重试机制，但极端网络环境下仍可能超时
