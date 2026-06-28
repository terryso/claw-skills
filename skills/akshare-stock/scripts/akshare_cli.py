#!/usr/bin/env python3
"""
A股量化数据分析 CLI —— 基于 AkShare

用法:
    python3 akshare_cli.py spot                          # 全市场实时行情
    python3 akshare_cli.py spot --board 北证A股           # 指定板块实时行情
    python3 akshare_cli.py kline 000001                   # 日K线（默认近一年）
    python3 akshare_cli.py kline 000001 --period weekly   # 周K线
    python3 akshare_cli.py kline 000001 --start 20240101 --end 20241231
    python3 akshare_cli.py finance 000001                 # 财务报表摘要
    python3 akshare_cli.py indicator 000001               # 主要财务指标
    python3 akshare_cli.py board                          # 行业板块列表
    python3 akshare_cli.py board --concept                # 概念板块列表
    python3 akshare_cli.py board --cons 半导体             # 板块内个股
    python3 akshare_cli.py fund 000001                    # 个股资金流向
    python3 akshare_cli.py lhb --date 20240930            # 龙虎榜
    python3 akshare_cli.py ipo                            # 新股申购
    python3 akshare_cli.py rzrq 600000                    # 融资融券

输出: JSON（默认）或表格（--format table）
"""

import argparse
import json
import sys
import time
import traceback
from datetime import datetime, timedelta


def get_ak():
    """导入 akshare，带友好错误提示。"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        print(json.dumps({"error": "akshare 未安装，请执行: pip install akshare"}, ensure_ascii=False))
        sys.exit(1)


def safe_call(fn, *args, retries=2, delay=1, **kwargs):
    """带重试的安全调用。AkShare 依赖网络抓取，偶尔会超时或被限流。"""
    last_err = None
    for attempt in range(retries + 1):
        try:
            df = fn(*args, **kwargs)
            if df is None or (hasattr(df, 'empty') and df.empty):
                return {"warning": "查询成功但无数据", "data": []}
            df = df.fillna("")  # NaN → 空字符串，避免 JSON 序列化问题
            records = df.to_dict(orient="records")
            return {"data": records, "count": len(records)}
        except Exception as e:
            last_err = str(e)
            if attempt < retries:
                time.sleep(delay * (attempt + 1))
    return {"error": f"重试 {retries} 次后仍失败: {last_err}"}


def cmd_spot(args):
    ak = get_ak()
    if args.board:
        return safe_call(ak.stock_zh_a_spot_em, symbol=args.board)
    return safe_call(ak.stock_zh_a_spot_em)


def cmd_kline(args):
    ak = get_ak()
    end = args.end or datetime.now().strftime("%Y%m%d")
    start = args.start or (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
    return safe_call(
        ak.stock_zh_a_hist,
        symbol=args.code,
        period=args.period,
        start_date=start,
        end_date=end,
        adjust=args.adjust,
    )


def cmd_finance(args):
    ak = get_ak()
    return safe_call(ak.stock_financial_abstract_ths, symbol=args.code, indicator="按报告期")


def cmd_indicator(args):
    ak = get_ak()
    return safe_call(ak.stock_financial_analysis_indicator, symbol=args.code)


def cmd_board(args):
    ak = get_ak()
    if args.cons:
        return safe_call(ak.stock_board_industry_cons_em, symbol=args.cons)
    if args.concept:
        return safe_call(ak.stock_board_concept_name_em)
    return safe_call(ak.stock_board_industry_name_em)


def cmd_fund(args):
    ak = get_ak()
    code = args.code
    market = "sh" if code.startswith(("5", "6", "9")) else "sz"
    return safe_call(ak.stock_individual_fund_flow, stock=code, market=market)


def cmd_lhb(args):
    ak = get_ak()
    date = args.date or datetime.now().strftime("%Y%m%d")
    return safe_call(ak.stock_lhb_detail_em, date=date)


def cmd_ipo(args):
    ak = get_ak()
    if args.upcoming:
        return safe_call(ak.stock_new_ipo_start_em)
    return safe_call(ak.stock_new_ipo_em)


def cmd_rzrq(args):
    ak = get_ak()
    code = args.code
    if code.startswith(("5", "6")):
        return safe_call(ak.stock_margin_sse, symbol=code)
    return safe_call(ak.stock_rzrq_detail_em, symbol=code, date=args.date or datetime.now().strftime("%Y%m%d"))


def print_result(result, fmt="json"):
    if fmt == "table":
        data = result.get("data", [])
        if not data:
            print(result.get("error") or result.get("warning") or "无数据")
            return
        if not data:
            return
        keys = list(data[0].keys())
        # 截断显示前 8 列
        show_keys = keys[:8]
        # 打印表头
        print("\t".join(str(k) for k in show_keys))
        print("-" * 80)
        for row in data[:50]:  # 最多显示 50 行
            print("\t".join(str(row.get(k, "")) for k in show_keys))
        if len(data) > 50:
            print(f"... 共 {len(data)} 条记录，仅显示前 50 条")
    else:
        print(json.dumps(result, ensure_ascii=False, default=str))


COMMANDS = {
    "spot": (cmd_spot, "实时行情"),
    "kline": (cmd_kline, "历史K线"),
    "finance": (cmd_finance, "财务报表摘要"),
    "indicator": (cmd_indicator, "主要财务指标"),
    "board": (cmd_board, "板块/行业分析"),
    "fund": (cmd_fund, "资金流向"),
    "lhb": (cmd_lhb, "龙虎榜"),
    "ipo": (cmd_ipo, "新股/IPO"),
    "rzrq": (cmd_rzrq, "融资融券"),
}


def main():
    parser = argparse.ArgumentParser(
        description="A股量化数据分析 CLI（AkShare）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # spot
    p = sub.add_parser("spot", help="实时行情")
    p.add_argument("--board", default=None, help="板块名称，如 '北证A股'")

    # kline
    p = sub.add_parser("kline", help="历史K线")
    p.add_argument("code", help="股票代码，如 000001")
    p.add_argument("--period", default="daily", choices=["daily", "weekly", "monthly"])
    p.add_argument("--start", default=None, help="开始日期 YYYYMMDD")
    p.add_argument("--end", default=None, help="结束日期 YYYYMMDD")
    p.add_argument("--adjust", default="qfq", choices=["qfq", "hfq", ""], help="复权方式")

    # finance
    p = sub.add_parser("finance", help="财务报表摘要")
    p.add_argument("code", help="股票代码")

    # indicator
    p = sub.add_parser("indicator", help="主要财务指标")
    p.add_argument("code", help="股票代码")

    # board
    p = sub.add_parser("board", help="板块/行业分析")
    p.add_argument("--concept", action="store_true", help="查询概念板块")
    p.add_argument("--cons", default=None, help="查询指定板块的个股，如 '半导体'")

    # fund
    p = sub.add_parser("fund", help="个股资金流向")
    p.add_argument("code", help="股票代码")

    # lhb
    p = sub.add_parser("lhb", help="龙虎榜")
    p.add_argument("--date", default=None, help="日期 YYYYMMDD")

    # ipo
    p = sub.add_parser("ipo", help="新股/IPO")
    p.add_argument("--upcoming", action="store_true", help="待上市新股")

    # rzrq
    p = sub.add_parser("rzrq", help="融资融券")
    p.add_argument("code", help="股票代码")
    p.add_argument("--date", default=None, help="日期 YYYYMMDD")

    # 全局参数
    parser.add_argument("--format", default="json", choices=["json", "table"], help="输出格式")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    handler, desc = COMMANDS[args.command]
    result = handler(args)
    print_result(result, args.format)

    # 如果有错误，exit code = 1
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
