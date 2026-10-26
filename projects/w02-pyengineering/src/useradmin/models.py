'''
Author: SCIICO 1114259706@qq.com
Date: 2026-10-19 09:53:33
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-10-26 10:50:45
FilePath: \ai-learning\\projects\\w02-pyengineering\\models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from dataclasses import dataclass
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)



class RegisterRequest(BaseModel):
    username: str
    password: str
    age: int = Field(ge=0, le=150)

@dataclass
class InternalUser:
    id: int
    username: str
    email: str
    activated: bool=False

def activate(u:InternalUser)->InternalUser:
    u.activated = True
    logger.info("user activated user_id=%s", u.id)
    return u

def parse_age(raw:str | None)->int | None:
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


if __name__ == "__main__":  #pragma: no cover
    r = RegisterRequest.model_validate(
        {"username":"sciico", "password":"123456", "age":"25"}
        )
    print(type(r.age),r.age)

    u = InternalUser(id=1, username="sciico", email="sciico@example.com")
    print(activate(u))

    print(parse_age("30"),parse_age("abc"),parse_age(None))



#RegisterRequest(username="x",email="sciico@example.com",age="abc")
#bad = InternalUser(id="oops", username=123, email="e")# type: ignore[arg-type]
#print(bad)