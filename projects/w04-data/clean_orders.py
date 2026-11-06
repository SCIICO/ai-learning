"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-06 11:51:10
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-06 11:54:04
FilePath: \ai-learning\\projects\\w04-data\\clean_order.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""clean_orders.py — 幂等清洗：脏 CSV → Parquet（row_id 贯穿全程）"""
import pandas as pd

RAW, OUT = "orders_dirty.csv", "clean_orders.parquet"


def main():
    df = pd.read_csv(RAW)
    df.insert(0, "row_id", df.index)  # 源行号主键，贯穿全程

    # 1) 日期解析：errors="coerce"，失败的变 NaT
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 2) 缺失值：先标记（缺失留痕），再用中位数填充
    df["amount_missing"] = df["amount"].isna()
    df["amount"] = df["amount"].fillna(df["amount"].median())

    # 3) 空串三连击：标记 → 翻译 → 填充
    df["city_missing"] = df["city"] == ""
    df["city"] = df["city"].replace("", pd.NA)
    df["city"] = df["city"].fillna("未知")

    # 4) 异常值：amount <= 0 按业务规则剔除
    bad = df["amount"] <= 0
    print(f"剔除异常行：{bad.sum()} 行")
    df = df[~bad]

    # 5) 类型优化
    df["city"] = df["city"].astype("category")
    df["category"] = df["category"].astype("category")

    # 6) 输出 Parquet
    df.to_parquet(OUT, index=False)
    print(f"清洗完成：{len(df)} 行 → {OUT}")

    # 7) 自检
    check = pd.read_parquet(OUT)
    check.info()


if __name__ == "__main__":
    main()
