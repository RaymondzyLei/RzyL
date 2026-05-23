import nonebot
from pathlib import Path
from .keywords import KEYWORDS

config = nonebot.get_driver().config

# 允许使用本插件的群聊列表，留空表示所有群聊都可以使用
ALLOWED_GROUPS = getattr(config, 'dawu_allowed_groups', []) or []

def get_image_path(keyword: str) -> Path:
    return Path.cwd() / "src" / "asserts" / "dawu" / f"{keyword}.jpg"