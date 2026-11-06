"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-06 09:09:50
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-06 10:38:30
FilePath: \ai-learning\\projects\\w04-data\\sql_review.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-06 09:09:50
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-06 10:28:26
FilePath: \ai-learning\\projects\\w04-data\\sql_review.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""
import duckdb

con = duckdb.connect()

ALL = [
    (
        1,
        "每城市销售额TOP2",
        """
SELECT * FROM(
    SELECT city,date,amount,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY amount DESC) AS rn
    FROM 'clean_orders.parquet'
)WHERE rn <= 2
ORDER BY city,rn
""",
    ),
    (
        2,
        "每城市按日期的累计销售额",
        """
SELECT city,date,amount,
    SUM(amount) OVER (PARTITION BY city ORDER BY date) AS 累计销售额
FROM 'clean_orders.parquet'
ORDER BY city,date
    """,
    ),
    (
        3,
        "每城市人均消费",
        """
SELECT
    o.city,
    SUM(o.amount)   AS 总销售额,
    MAX(p.population)   AS 人口,
    ROUND(SUM(o.amount)/MAX(p.population),2)    AS 人均消费
FROM 'clean_orders.parquet' AS o
JOIN 'city_pop.csv' AS p
ON o.city = p.city
GROUP BY o.city
ORDER BY 人均消费 DESC
    """,
    ),
    (
        4,
        "城市×品类 CASE WHEN 手工透视",
        """
SELECT
    city,
    SUM(CASE WHEN category = '数码' THEN amount ELSE 0 END) AS "数码",
    SUM(CASE WHEN category = '食品' THEN amount ELSE 0 END) AS "食品",
    SUM(CASE WHEN category = '服饰' THEN amount ELSE 0 END) AS "服饰",
    SUM(amount)                             AS  合计
FROM 'clean_orders.parquet'
GROUP BY city
    """,
    ),
    (
        5,
        "去重城市数量",
        """
SELECT
    COUNT(DISTINCT city)    AS  城市数量
FROM 'clean_orders.parquet'
    """,
    ),
]


def q(n, title, sql):
    print(f"\n==题{n}·{title} ==")
    print(con.sql(sql).df())


for n, title, sql in ALL:
    q(n, title, sql)
