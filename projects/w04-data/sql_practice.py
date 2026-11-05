"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-05 09:03:45
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-05 14:11:03
FilePath: \ai-learning\\projects\\w04-data\\sql_practice.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""sql_practice.py -- W4D4 SQL 实战 15 题"""

import duckdb

con = duckdb.connect()  # 显式建连接

ALL = [
    (
        1,
        "总览",
        """
SELECT
    SUM(amount) AS 总销售额,
    COUNT(*)    AS 订单数,
    ROUND(AVG(amount),2)    AS 平均单额
FROM 'clean_orders.parquet'
""",
    ),
    (
        2,
        "销售额降序排序",
        """
SELECT
    city,
    COUNT(*)    AS 订单数,
    SUM(amount) AS 总销售额
FROM 'clean_orders.parquet'
GROUP BY city
ORDER BY 总销售额 DESC
""",
    ),
    (
        3,
        "平均单额",
        """
SELECT
    category,
    ROUND(AVG(amount),2)    AS 平均单额
FROM'clean_orders.parquet'
GROUP BY category
ORDER BY 平均单额 DESC
""",
    ),
    (
        4,
        "销售额最高的两个城市",
        """
SELECT
    city,
    SUM(amount) AS 总销售额
FROM 'clean_orders.parquet'
GROUP BY city
ORDER BY 总销售额 DESC LIMIT 2
""",
    ),
    (
        5,
        "在100-300的订单数",
        """
SELECT
    COUNT(*) AS 订单数
FROM 'clean_orders.parquet'
WHERE amount BETWEEN 100 AND 300
""",
    ),
    (
        6,
        "每个城市的数码品类订单数与总额",
        """
SELECT
    city,
    COUNT(*) AS 订单数,
    SUM(amount) AS 订单总额
FROM 'clean_orders.parquet'
WHERE category = '数码'
GROUP BY city
ORDER BY 订单总额 DESC
""",
    ),
    (
        7,
        "城市名以「北」开头的订单",
        """
SELECT
    date,city,category,amount,
FROM 'clean_orders.parquet'
WHERE city  LIKE '北%'
""",
    ),
    (
        8,
        "去重+城市数量",
        """
SELECT
    COUNT(DISTINCT city) AS 城市数量
FROM 'clean_orders.parquet'
""",
    ),
    (
        9,
        "订单连接 city_pop.csv，输出带人口列",
        """
SELECT
    o.date,
    o.city,
    o.amount,
    p.population
FROM 'clean_orders.parquet' AS o
JOIN 'city_pop.csv' AS p
ON o.city = p.city
""",
    ),
    (
        10,
        "每城市人均消费",
        """
SELECT
    o.city,
    SUM(o.amount)   AS 总销售额,
    MAX(p.population) AS 人口,
    ROUND(SUM(o.amount)/MAX(p.population),2) AS 人均消费
FROM 'clean_orders.parquet' AS o
JOIN 'city_pop.csv' AS p
ON o.city = p.city
GROUP BY o.city
ORDER BY 人均消费 DESC
""",
    ),
    (
        11,
        "城市销售额TOP 2订单",
        """
SELECT * FROM(
    SELECT city,date,amount,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY amount DESC) AS rn
    FROM 'clean_orders.parquet'
)WHERE rn<=2
ORDER BY city,rn
""",
    ),
    (
        12,
        "每城市按日期的累计销售额",
        """
    SELECT city,date,amount,
        SUM(amount) OVER (PARTITION BY city ORDER BY date) AS 累计销售额
    FROM 'clean_orders.parquet'
    ORDER BY city,date
""",
    ),
    (
        13,
        "每订单的城市内销售额排名 + 全表排名（两个窗口同列输出）",
        """
SELECT
    city,
    date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY city ORDER BY amount DESC) AS rn_city,
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS rn_all
FROM 'clean_orders.parquet'
ORDER BY city,rn_city
""",
    ),
    (
        14,
        "每城市的订单日期跨度（最早日期、最晚日期、相隔天数）",
        """
SELECT
    city,
    MIN(date)   AS  最早日期,
    MAX(date)   AS  最晚日期,
    DATE_DIFF('day',MIN(date),MAX(date))    AS  相隔天数
FROM 'clean_orders.parquet'
GROUP BY city
""",
    ),
    (
        15,
        "城市X品类销售额手工透视",
        """
SELECT
    city,
    SUM(CASE WHEN category = '数码' THEN amount ELSE 0 END) AS "数码",
    SUM(CASE WHEN category = '食品' THEN amount ELSE 0 END) AS "食品",
    SUM(CASE WHEN category = '服饰' THEN amount ELSE 0 END) AS "服饰",
    SUM(amount)                                             AS 合计
FROM 'clean_orders.parquet'
GROUP BY city
""",
    ),
]


def q(n, title, sql):
    print(f"\n==题{n}·{title} ==")
    print(con.sql(sql).df())


for n, title, sql in ALL:
    q(n, title, sql)
