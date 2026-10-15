# ai-learning

30 周 AI 转岗学习大本营（LLM 应用工程师 × MLOps/AI 平台双轨）。

计划周期：2026-10-16 → 2027-05-09

## 目录规划

```
ai-learning/
├── .venv/              # Python 虚拟环境（uv 管理，勿提交）
├── notes/              # 学习笔记（按 阶段/主题/踩坑 三层组织）
├── projects/           # 各阶段项目
│   ├── stage1-package/       # 阶段 1：规范 Python 包
│   ├── stage2-ml/            # 阶段 2：结构化建模 + Transformer
│   ├── stage3-service/       # 阶段 3：FastAPI 推理服务
│   └── flagship/             # 阶段 6：旗舰项目
└── daily/              # 每日练习与验证脚本
```

## 环境说明

- Python：3.13.9（系统安装）
- 虚拟环境：`uv venv` 创建于 `.venv/`
- 激活：`.venv\Scripts\activate`（PowerShell / CMD）或 `source .venv/Scripts/activate`（Git Bash）
- 安装依赖：`uv pip install <pkg>`
