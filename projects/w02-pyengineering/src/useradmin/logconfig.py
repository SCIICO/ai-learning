'''
Author: SCIICO 1114259706@qq.com
Date: 2026-10-27 10:12:42
LastEditors: SCIICO 1114259706@qq.com
LastEditTime: 2026-10-27 10:15:08
FilePath: \ai-learning\\projects\\w02-pyengineering\\src\\useradmin\\logconfig.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import logging

from useradmin.config import settings

def setup_logging() -> None:
    """按 settings 统一配置日志格式与级别"""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )