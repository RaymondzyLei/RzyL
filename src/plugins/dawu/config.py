import nonebot
from pathlib import Path
from .keywords import KEYWORDS

config = nonebot.get_driver().config

# 允许使用本插件的群聊列表，从环境变量获取
# 在 .env 中设置：DAWU_ALLOWED_GROUPS=123456789,987654321
# 留空或未设置表示所有群聊都可以使用
ALLOWED_GROUPS = []
if hasattr(config, 'dawu_allowed_groups'):
    groups = config.dawu_allowed_groups
    if groups:
        if isinstance(groups, list):
            ALLOWED_GROUPS = groups
        elif isinstance(groups, int):
            ALLOWED_GROUPS = [groups]
        elif isinstance(groups, str):
            ALLOWED_GROUPS = [int(g.strip()) for g in groups.split(',') if g.strip().isdigit()]

#`src\asserts\dawu\`下的图片文件名与"'KEYWORDS中的第一个对象'+'.jpg'"相同
def get_image_path(keyword: str) -> Path:
    return Path.cwd() / "src" / "asserts" / "dawu" / f"{keyword}.jpg"
