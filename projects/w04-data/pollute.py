"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-03 09:41:05
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-03 10:47:58
FilePath: \ai-learning\\projects\\w04-data\\pollute.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""在干净的 orders.csv 基础上注入四类脏数据 """
import pandas as pd

df = pd.read_csv("orders.csv")
df.loc[3, "amount"] = None  # 缺失值
df.loc[7, "amount"] = -50  # 异常值（业务不可能）
df.loc[11, "city"] = ""  # 空串伪装成有值
df.loc[15, "date"] = "2026-10-99"  # 日期格式不一致
df.to_csv("orders_dirty.csv", index=False, encoding="utf-8-sig")
print("脏数据已注入：1缺失 / 1异常 / 1空串 / 1日期格式 ")
