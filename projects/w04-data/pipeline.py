"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-09 09:18:08
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-09 09:58:57
FilePath: \ai-learning\\projects\\w04-data\\pipeline.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import argparse
import subprocess
import sys
from pathlib import Path

# CWD 铁律的工程化解法：以本文件所在的目录为锚点
# 无论从哪个目录启动pipeline.py 子脚本都在正确的工作目录跑

BASE = Path(__file__).resolve().parent

# 数据驱动：步骤表以后加一步只需在这里加一行
STEPS = {
    "gen": "gen_data.py",
    "pollute": "pollute.py",
    "clean": "clean_orders.py",
    "analyze": "analysis.py",
}


def run_step(name: str) -> None:
    """运行单个脚本步骤。check=True:一步失败立即停，不带病运行"""
    script = STEPS[name]
    print(f"\n=====步骤[{name}]->{script}=====")
    subprocess.run([sys.executable, script], cwd=BASE, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="w04 数据管道主入口")
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    # 用循环批两注册四个单步子命令（和STEPS字典保持同源）
    for name in STEPS:
        sub.add_parser(name, help=f"只跑{name}这一步")
    # gen 预留参数：gen_data.py 目前写死 n=60,函数化改造后才能接入
    sub.choices["gen"].add_argument("--rows", type=int, default=None)
    sub.add_parser("all", help="端到端跑完全部步骤")

    args = parser.parse_args()

    if args.command == "all":
        for name in STEPS:
            run_step(name)
        print(
            "\n✅ 端到端完成：orders.csv → orders_dirty.csv → clean_orders.parquet → 分析输出"
        )
    else:
        run_step(args.command)


if __name__ == "__main__":
    main()
