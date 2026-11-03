"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-03 10:01:22
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-03 10:02:35
FilePath: \ai-learning\\projects\\w04-data\\dignose.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import pandas as pd

df = pd.read_csv("orders_dirty.csv")
df.info()
df.isna().sum()
df.describe()
