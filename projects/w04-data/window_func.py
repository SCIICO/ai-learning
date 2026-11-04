import duckdb
import numpy as np
import pandas as pd

df = pd.read_parquet("clean_orders.parquet")

# ———— 验证1：聚合 OVER ≈ transform ————————————————————
sql1 = """
SELECT city,amount,
        AVG(amount) OVER (PARTITION BY city) AS city_avg
FROM 'clean_orders.parquet'
"""

r1 = duckdb.sql(sql1).df()
print(r1.head())

# Pandas 版对照
p1 = df[["city", "amount"]].copy()
p1["city_avg"] = df.groupby("city")["amount"].transform("mean")
print(
    "与Pandas transform 结果一致：",
    r1.sort_values(["city", "amount"])
    .reset_index(drop=True)
    .equals(p1.sort_values(["city", "amount"]).reset_index(drop=True)),
)


# ———— 验证 2 ： ROW_NUMBER + 每城市 Top-2 ——————
sql2 = """
SELECT * FROM(
    SELECT city,date,amount,
            ROW_NUMBER() OVER (PARTITION BY city ORDER BY amount DESC) AS rn
    FROM 'clean_orders.parquet'
) WHERE rn <=2
ORDER BY city,rn
"""
print("\n—— 每城市销售额 Top-2 ——")
print(duckdb.sql(sql2).df())

# ———— 验证 3 : LAG 环比 ————————————————————
sql3 = """
SELECT city,date,amount,
        LAG(amount) OVER (PARTITION BY city ORDER BY date)  AS prev_amount,
        amount - LAG(amount) OVER (PARTITION BY city ORDER BY date) AS diff
FROM 'clean_orders.parquet'
ORDER BY city,date
"""


print("\n————LAG 环比 ————")
print(duckdb.sql(sql3).df())


a = r1.sort_values(["city", "amount"]).reset_index(drop=True)["city_avg"]
b = p1.sort_values(["city", "amount"]).reset_index(drop=True)["city_avg"]

print("最大绝对偏差：", (a - b).abs().max())
print("容差内一致：", np.allclose(a, b))
