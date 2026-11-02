""" " gen_data.py - 生成练习数据"""

import numpy as np
import pandas as pd

np.random.seed(42)
n = 60
df = pd.DataFrame(
    {
        "date": pd.date_range("2026-10-01", periods=n, freq="6h").date,
        "city": np.random.choice(["北京", "上海", "深圳"], n),
        "category": np.random.choice(["数码", "食品", "服饰"], n),
        "amount": np.random.randint(50, 500, n),
    }
)
df.to_csv("orders.csv", index=False, encoding="utf-8-sig")
print(df.head())
