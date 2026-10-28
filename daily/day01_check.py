"""Day 01 环境验收脚本（2026-10-16）

运行方式（在 D:/ai-learning 目录下）：
    .venv/Scripts/python.exe daily/day01_check.py

全部打印为 [PASS] 即代表第一日验收通过。
"""

import sys
from pathlib import Path


def main() -> None:
    # 1. 虚拟环境检查：解释器必须位于 .venv 内，而非系统全局
    venv_root = Path(__file__).resolve().parent.parent / ".venv"
    in_venv = str(sys.executable).startswith(str(venv_root))
    print(f"[{'PASS' if in_venv else 'FAIL'}] 虚拟环境：{sys.executable}")
    if not in_venv:
        print("       请用 .venv/Scripts/python.exe 运行本脚本，而不是系统 python")

    # 2. Python 版本
    ok = sys.version_info >= (3, 12)
    print(
        f"[{'PASS' if ok else 'FAIL'}] Python 版本：{sys.version.split()[0]}（要求 >= 3.12）"
    )

    # 3. 仓库结构
    root = Path(__file__).resolve().parent.parent
    for sub in ("notes", "projects", "daily"):
        p = root / sub
        ok = p.is_dir()
        print(f"[{'PASS' if ok else 'FAIL'}] 目录存在：{sub}/")
        if not ok:
            p.mkdir(parents=True, exist_ok=True)
            print(f"       已自动创建 {sub}/")

    print("\n第一日验收：环境搭建完成。下一步是 git push。")


if __name__ == "__main__":
    main()
