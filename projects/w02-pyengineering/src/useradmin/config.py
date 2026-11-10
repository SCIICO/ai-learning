"""
Author: SCIICO 1114259706@qq.com
Date: 2026-10-29 10:36:47
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-11-10 10:08:57
FilePath: \ai-learning\\projects\\w02-pyengineering\\src\\useradmin\\config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="USERADMIN_")
    app_name: str = "useradmin"
    debug: bool = False
    log_level: str = "INFO"
    secret_key: str = Field(default="", repr=False)

    @field_validator("secret_key")
    @classmethod
    def secret_key_required(cls, v: str) -> str:
        if not v:
            raise ValueError("USERADMIN_SECRET_KEY 未设置：检查.env或环境变量")
        return v


settings = Settings()
