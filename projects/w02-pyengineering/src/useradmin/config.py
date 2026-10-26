'''
Author: SCIICO 1114259706@qq.com
Date: 2026-10-26 10:37:34
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-10-26 10:46:31
FilePath: \ai-learning\\projects\\w02-pyengineering\\src\\useradmin\\config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="USERADMIN_")
    app_name: str = "useradmin"
    debug: bool = False
    log_level: str = "INFO"

settings = Settings()