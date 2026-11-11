"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-10 10:51:12
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-10 11:00:59
FilePath: \ai-learning\\projects\\w04-data\try.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import duckdb

r1 = duckdb.sql("""
    SELECT
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY amount DESC) AS rn,
        city,
        amount
    FROM 'orders.csv'
    ORDER BY city,rn
    """).df()
print(r1)


r2 = duckdb.sql("""
    SELECT
        date,city,amount,
        LAG(amount) OVER (PARTITION BY city ORDER BY date,city) AS prev_amount,
        amount - LAG(amount) OVER (ORDER BY date) AS diff
    FROM 'orders.csv'
    ORDER BY date,city
    """).df()

print(r2)
