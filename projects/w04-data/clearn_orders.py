"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-03 10:02:59
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-03 10:51:50
FilePath: \ai-learning\\projects\\w04-data\\clear_orders.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

""" claer_orders.py - 幂等清洗：脏CSV - Parquet"""
import pandas as pd

RAW, OUT = "orders_dirty.csv", "clean_orders.parquet"


def main():
    df = pd.read_csv(RAW)

    # 1) 日期解析：errors="coerce",失败变NaT
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 2) 缺失值：amount 用中位数填充，并加标记列（策略三选哪一种？你来定并写注释说明理由）
    df["amount_missing"] = df["amount"].isna()  # True = 缺失
    df["amount"] = df["amount"].fillna(df["amount"].median())

    # 3) 空串处理：city 的 "" 是「伪装成有值的缺失」——你想删行、填充还是标记？
    df["city_missing"] = df["city"] == ""  # True = 这行是空串
    df["city"] = df["city"].replace("", pd.NA)
    df["city"] = df["city"].fillna("未知")  # 填未知而非删除

    # 4) 异常值：amount <= 0 的行按业务规则剔除（记录剔了几行）
    bad = df["amount"] <= 0
    print(f"剔除异常行：{bad.sum()}行")  # 预期1(-50那行)
    df = df[~bad]  # ~ = 取反,保留[不是异常]的行

    # 5) 类型优化：city/category 转 category
    df["city"] = df["city"].astype("category")
    df["category"] = df["category"].astype("category")

    # 6)输出 Parquet
    df.to_parquet(OUT, index=False)
    print(f"清洗完成：{len(df)}行-{OUT}")

    # 7)自检：重读一遍验证类型与内容
    check = pd.read_parquet(OUT)
    check.info()


if __name__ == "__main__":
    main()
