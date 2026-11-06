"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-06 11:55:09
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-06 11:55:16
FilePath: \ai-learning\\projects\\w04-data\\strip_invisible.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""strip_invisible.py — 清除文件中的零宽/隐形字符（粘贴去污器）"""
import pathlib
import sys

p = pathlib.Path(sys.argv[1])
text = p.read_text(encoding="utf-8")

INVISIBLE = [
    "\u200b",  # 零宽空格
    "\u200c",  # 零宽非连接符
    "\u200d",  # 零宽连接符
    "\u2060",  # 文字连接符
    "\ufeff",  # BOM/零宽不换行空格
    "\u00ad",  # 软连字符
]

cleaned = text
for ch in INVISIBLE:
    cleaned = cleaned.replace(ch, "")

p.write_text(cleaned, encoding="utf-8")
print(f"清除了 {len(text) - len(cleaned)} 个隐形字符")
