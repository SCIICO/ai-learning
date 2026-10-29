"""
Author: SCIICO 1114259706@qq.com
Date: 2026-10-26 10:37:34
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-10-27 10:10:59
FilePath: \ai-learning\\projects\\w02-pyengineering\\src\\useradmin\\config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="USERADMIN_")
    app_name: str = "useradmin"
    debug: bool = False
    log_level: str = "INFO"
    secret_key: str


settings = Settings()


"""<!--
 * @Author: SCIICO 1114259706@qq.com
 * @Date: 2026-10-15 14:01:56
 * @LastEditors: SCIICO 1114259706@qq.com
 * @LastEditTime: 2026-10-23 09:54:25
 * @FilePath: \ai-learning\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
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



#   useradmin

- 用户注册场景的类型安全数据模型包：pydantic 左边界校验，dataclass 管内部数据 ，mypy全绿

##  功能特性

- 100% 静态类型检查通过（mypy），测试覆盖率 100%
- 14 个 pytest 测试全绿，覆盖三分支与全部校验边界（0/150/缺字段/非法类型）
- 边界数据自动校验：非法输入当场抛ValidationError，字符串年龄自动转 int


##  安装
 ````bash
git clone https://github.com/SCIICO/ai-learning.git
cd ai-learning/projects/w02-pyengineering
uv sync
 ````

##  快速开始

 ````python
from useradmin import RegisterRequest

#合法数据：字符串年龄被自动转换为 int
r = RegisterRequest.model_validate(
    {"username":"sciico","password":"123456","age":"25“}
)
print(type(r.age),r.age)  #<class 'int'>25
 ````

 非法数据会被当场拦截

  ````python
  from useradmin import RegisterRequest

  RegisterRequest.model_validate({"username":"u","password":"p","age":"abc"})
  # pydantic_core.ValidationError:Input should be a valid integer...
 ````

##  运行测试
 ````bash
 uv run pytest -v --cov=useradmin --cov-report=term-missing
  ````

当前状态：**14 passed,覆盖率 100%**('__main__' 演示模块已用 pragma 显示排除)

## 目录结构

```
w02-pyengineering/
├── pyproject.toml          # 项目元数据与依赖声明
├── uv.lock                 # 依赖锁文件（精确版本）
├── README.md
├── src/useradmin/          # 包本体
│   ├── __init__.py         # 对外导出（门面）
│   └── models.py           # 数据模型
└── tests/
    └── test_models.py      # 14 个测试
    <!--
 * @Author: SCIICO 1114259706@qq.com
 * @Date: 2026-10-15 14:01:56
 * @LastEditors: SCIICO 1114259706@qq.com
 * @LastEditTime: 2026-10-23 09:54:25
 * @FilePath: \ai-learning\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
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



#   useradmin

- 用户注册场景的类型安全数据模型包：pydantic 左边界校验，dataclass 管内部数据 ，mypy全绿

##  功能特性

- 100% 静态类型检查通过（mypy），测试覆盖率 100%
- 14 个 pytest 测试全绿，覆盖三分支与全部校验边界（0/150/缺字段/非法类型）
- 边界数据自动校验：非法输入当场抛ValidationError，字符串年龄自动转 int


##  安装
 ````bash
git clone https://github.com/SCIICO/ai-learning.git
cd ai-learning/projects/w02-pyengineering
uv sync
 ````

##  快速开始

 ````python
from useradmin import RegisterRequest

#合法数据：字符串年龄被自动转换为 int
r = RegisterRequest.model_validate(
    {"username":"sciico","password":"123456","age":"25“}
)
print(type(r.age),r.age)  #<class 'int'>25
 ````

 非法数据会被当场拦截

  ````python
  from useradmin import RegisterRequest

  RegisterRequest.model_validate({"username":"u","password":"p","age":"abc"})
  # pydantic_core.ValidationError:Input should be a valid integer...
 ````

##  运行测试
 ````bash
 uv run pytest -v --cov=useradmin --cov-report=term-missing
  ````

当前状态：**14 passed,覆盖率 100%**('__main__' 演示模块已用 pragma 显示排除)

## 目录结构

```
w02-pyengineering/
├── pyproject.toml          # 项目元数据与依赖声明
├── uv.lock                 # 依赖锁文件（精确版本）
├── README.md
├── src/useradmin/          # 包本体
│   ├── __init__.py         # 对外导出（门面）
│   └── models.py           # 数据模型
└── tests/
    └── test_models.py      # 14 个测试
```

```
"""
