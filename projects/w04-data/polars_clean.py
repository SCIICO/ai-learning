"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-06 10:32:41
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-06 12:03:44
FilePath: \ai-learning\\projects\\w04-data\\polars_clean.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import pandas as pd
import polars as pl

a = (
    pl.read_parquet("clean_orders_polars.parquet")
    .to_pandas()
    .sort_values(["date", "city", "amount"])
    .reset_index(drop=True)
)
b = (
    pd.read_parquet("clean_orders.parquet")
    .sort_values(["date", "city", "amount"])
    .reset_index(drop=True)
)

print("amount 最大偏差：", (a["amount"] - b["amount"]).abs().max())
print("city 逐值一致：", (a["city"].astype(str) == b["city"].astype(str)).all())
print("date 逐值一致：", (a["date"] == b["date"]).all())

RAW, OUT = "orders_dirty.csv", "clean_orders_polars.parquet"

lf = (
    pl.scan_csv(RAW)
    .with_row_index("row_id")
    .with_columns(
        pl.col("date").str.to_datetime(format="%Y-%m-%d", strict=False),
        pl.col("amount").is_null().alias("amount_missing"),
        (pl.col("city") == "").alias("city_missing"),
    )
    .with_columns(
        pl.col("city").replace("", None),
    )
    .with_columns(
        pl.col("amount").fill_null(pl.col("amount").median()),
        pl.col("city").fill_null("未知"),
    )
    .filter(pl.col("amount") > 0)
    .with_columns(
        pl.col("city").cast(pl.Categorical),
        pl.col("category").cast(pl.Categorical),
    )
)

clean = lf.collect()
clean.write_parquet(OUT)
print(f"清洗完成：{clean.height}行 - {OUT}")
print(clean.head())
print(clean.schema)


a = pl.read_parquet("clean_orders_polars.parquet").to_pandas().sort_values("row_id")
b = pd.read_parquet("clean_orders.parquet").sort_values("row_id")

m = a.merge(b, on="row_id", suffixes=("_pola", "_pand"))
print("配对行数：", len(m))  # 预期 59（一一对应，无膨胀）

print("amount 差异行：", ((m["amount_pola"] - m["amount_pand"]).abs() > 1e-9).sum())
print(
    "city   差异行：", (m["city_pola"].astype(str) != m["city_pand"].astype(str)).sum()
)
print("date   差异行：", (m["date_pola"] != m["date_pand"]).sum())

if (m["amount_pola"] - m["amount_pand"]).abs().max() > 0:
    print(
        m.loc[
            (m["amount_pola"] - m["amount_pand"]).abs() > 1e-9,
            ["row_id", "date", "city", "amount_pola", "amount_pand"],
        ]
    )
