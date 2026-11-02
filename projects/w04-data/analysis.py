"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-02 10:52:24
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-02 12:04:54
FilePath: \ai-learning\\projects\\w04-data\analysis.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import pandas as pd

df = pd.read_csv("orders.csv")

# 任务 1（agg）：每城市订单数 + 总销售额，降序
t1 = (
    df.groupby("city")["amount"]
    .agg(订单数="count", 总销售额="sum")
    .sort_values("总销售额", ascending=False)
)
# print("———— 任务1：agg分组汇总 ————")
# print(t1)


# 任务 2（transform）：加 city_avg 列 —— for 版 vs 一行 transform 版 对比
city_avg_map = {}
for city in df["city"].unique():
    city_avg_map[city] = df.loc[df["city"] == city, "amount"].mean()
for_result = df["city"].map(city_avg_map)

vec_result = df.groupby("city")["amount"].transform("mean")

df["city_avg"] = vec_result
print("———— 任务2：transform对比 ————")
print(vec_result)
print("两种写法结果一致：", for_result.equals(vec_result))
# 任务 3（merge）：自造 city_pop.csv（城市,人口），how="inner" vs "left" 行数对比

city_pop = pd.DataFrame(
    {"city": ["北京", "上海", "广州"], "population": [2189, 2487, 1874]}
)
inner = pd.merge(df, city_pop, on="city", how="inner")
left = pd.merge(df, city_pop, on="city", how="left")
print("inner 行数:", len(inner))  # 预期 < 60（深圳订单被剔除）
print("left  行数:", len(left))  # 预期 = 60（左表全量）

print(left[left["city"] == "深圳"].head())

# 任务 4（pivot_table）：城市 × 品类销售额透视，margins=True
pvt = df.pivot_table(
    index="city",
    columns="category",
    values="amount",
    aggfunc="sum",
    margins=True,
    fill_value=0,
)
print(pvt)
