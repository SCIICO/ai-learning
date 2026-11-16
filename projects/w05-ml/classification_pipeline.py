"""
Author: SCIICO 1114259706@qq.com
Date: 2026-11-12 13:55:07
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-12 14:56:29
FilePath: \ai-learning\\projects\\w05-ml\\classification_pipeline.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""classification_pipeline.py - Day 026: Pipeline 全流程建模（乳腺癌二分类）

泄漏防线：标准化与建模捆入 Pipeline，交叉验证每折内部重新 fit 变换。
流程：拆分 → CV(仅训练集) → 最终训练/考试 → 混淆矩阵 + 学习曲线。
"""


import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import (
    KFold,
    cross_val_score,
    learning_curve,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

RANDOM_STATE = 42

# 1、数据：sklearn 自带的真是医疗数据集
X, y = load_breast_cancer(return_X_y=True)
print(f"数据集：{X.shape[0]} 样本 x{X.shape[1]}特征")
print(
    f"类别分布：{np.bincount(y)} (0=恶性{np.bincount(y)[0]},1=良性{np.bincount(y)[1]})"
)

# 2、拆分：先隔离最终考场，stratify=y 保持类别比例
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

# 3、Pipline：标准化+逻辑回归，变换参数旨在训练折内学习，堵死泄漏
pipe = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000)),
    ]
)

# 4、只用训练集做5折交叉验证（选型/调参区）
cv_scores = cross_val_score(pipe, X_train, y_train, cv=5)
print(f"5折 CV 分数：{cv_scores.round(4)}")
print(f"CV 均值：{cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# 5、最终考试：fit 只见数据训练，score 时测试数据只被 predict
pipe.fit(X_train, y_train)
test_score = pipe.score(X_test, y_test)
print(f"测试集 accuracy:{test_score:.4f}")

# 6、混淆矩阵：看四种错误各有多少
fig1, ax1 = plt.subplots(figsize=(5, 4))
ConfusionMatrixDisplay.from_estimator(pipe, X_test, y_test, ax=ax1, colorbar=False)
ax1.set_title("混淆矩阵(测试集)")
fig1.tight_layout()
fig1.savefig("confusion_matrix.png", dpi=120)

# 7、学习曲线：昨天的方法，模型换成pipeline：cv打乱
sizes, train_s, val_s = learning_curve(
    pipe,
    X_train,
    y_train,
    train_sizes=np.linspace(0.1, 0.8),
    cv=KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
    scoring="accuracy",
)

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.plot(sizes, train_s.mean(axis=1), "o-", label="训练集 accuracy")
ax2.plot(sizes, val_s.mean(axis=1), "s-", label="验证集 accuracy")
ax2.set_xlabel("训练样本数")
ax2.set_ylabel("accuracy")
ax2.set_title("学习曲线（Pipeline 全流程）")
ax2.legend()
ax2.grid(alpha=0.3)
fig2.tight_layout()
fig2.savefig("learning_curve.png", dpi=120)

print("已保存 confusion_matrix.png / learning_curve.png")
