"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-11 10:02:50
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-11 10:57:34
FilePath: \ai-learning\\projects\\w05-ml\\learning_curve_demo.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""同一段数据，故意造两种病：作图高偏差（直线拟合正弦），右图高方差（15次多项式）"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import learning_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

rng = np.random.RandomState(42)
X = np.linspace(0, 1, 200).reshape(-1, 1)
y = np.sin(2 * np.pi * X).ravel() + rng.normal(0, 0.15, 200)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

for ax, degree, title in [
    (axes[0], 1, "degree=1 直线（高偏差/欠拟合）"),
    (axes[1], 15, "degree=15 多项式（高方差/过拟合）"),
]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    sizes, train_s, val_s = learning_curve(
        model, X, y, train_sizes=np.linspace(0.1, 1.0, 8), cv=10, scoring="r2"
    )
    ax.plot(sizes, train_s.mean(axis=1), "o-", label="训练集 R²")
    ax.plot(sizes, val_s.mean(axis=1), "s-", label="验证集 R²")
    ax.set_title(title)
    ax.set_xlabel("训练样本数")
    ax.set_ylabel("R²")
    ax.legend()
    ax.grid(alpha=0.3)


plt.tight_layout()
plt.savefig("learning_curves.png", dpi=120)
print("已保存 learning_curves.png")
