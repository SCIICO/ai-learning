'''
Author: SCIICO 1114259706@qq.com
Date: 2026-10-21 09:54:29
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-10-21 10:56:15
FilePath: \ai-learning\projects\w02-pyengineering\tests\test_models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
from pydantic import ValidationError

from useradmin.models import (
    InternalUser,
    RegisterRequest,
    activate,
    parse_age,
)

# 1)fixture : 给多个测试复用的现成用户
@pytest.fixture
def sample_user() -> InternalUser:
    return InternalUser(
        id = 1,
        username="sciico",
        email="sciico@example.com"
    )

#2)参数化: parse_age 的多组输入()
@pytest.mark.parametrize("raw,expected", [
    ("25", 25),
    ("0", 0),
    (None, None),
    ("abc",None)
])
def test_parse_age(raw:str | None , expected:int | None) -> None:
    assert parse_age(raw) == expected


#3)fixture 使用+状态变更验证
def test_activate(sample_user:InternalUser) -> None:
    result = activate(sample_user)
    assert result.activated is True

#4异常路径:两个ValidationError场景
def test_register_rejects_bad_age() -> None:
    with pytest.raises(ValidationError):
        RegisterRequest(username="sciico", password="123456", age=-1)

def test_register_rejects_all_fields() -> None:
    with pytest.raises(ValidationError):
        RegisterRequest(username="sciico", age=20)