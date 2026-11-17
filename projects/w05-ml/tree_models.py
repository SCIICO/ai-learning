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
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    KFold,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

RANDOM_STATE = 42

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# 数据：这次要拿特征名（画重要性图），不用return_X_y 简写
bunch = load_breast_cancer()
X, y = bunch.data, bunch.target
feat_names = bunch.feature_names
print(f"数据集：{X.shape[0]} 样本 x{X.shape[1]}特征")

# 拆分：与Day 026相同（同seed、同stratify）-对比才公平
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
# 三模型：唯一变量是模型
#   -逻辑回归带scaler（w·x 依赖量纲，Day 026已立法）
#   -树不带scaler（只做大小比较，理论免疫）
#   -XGBoost 三参数 = 棒数/步长/没棒深度（必须浅）

models = {
    "逻辑回归（基线）": Pipeline(
        [("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))]
    ),
    "随机森林": RandomForestClassifier(
        n_estimators=100, max_features="sqrt", random_state=RANDOM_STATE
    ),
    "XGBoost": XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.05,
        random_state=RANDOM_STATE,
        eval_metric="logloss",
    ),
}

# 统一设置 CV 设置（打乱）
cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

print("\n=== 三模型公平对比 ===")
results = {}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=cv)
    model.fit(X_train, y_train)
    test_score = model.score(X_test, y_test)
    results[name] = (scores.mean(), scores.std(), test_score)
    print(
        f"{name:<12}CV={scores.mean():.4f} ± {scores.std():.4f}"
        f"测试集={test_score:.4f}"
    )

# 特征重要性 Top-5 (随机森林的 feature_importances_)
rf = models["随机森林"]
importances = rf.feature_importances_

# argsort 升序排索引，[：：-1] 反转为降序，取前五
top5_idx = np.argsort(importances)[::-1][:5]

print("\n=== 随机森林 Top-5 特征 ===")
for rank, i in enumerate(top5_idx, start=1):
    print(f"{rank}: {feat_names[i]:<22} {importances[i]:.4f}")

fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(
    [feat_names[i] for i in top5_idx[::-1]],
    [importances[i] for i in top5_idx[::-1]],
    color="#2563eb",
)
ax.set_xlabel("重要性(feature_importances_)")
ax.set_title("随机森林 Top-5 特征重要性")
fig.tight_layout()
fig.savefig("feature_importance.png", dpi=120)

print("\n已保存 feature_importance.png")
