from nonebot import require
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from pathlib import Path

from .keywords import EASTER_EGG_KEYWORDS
from .random_text import load_random_text as try_load_random_text

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Alconna, Args, Match, on_alconna

__plugin_meta__ = PluginMetadata(
    name="彩蛋插件",
    description="迪士尼角色彩蛋查询与随机文本",
    usage="发送 彩蛋 <角色名> 查询迪士尼角色图片",
    type="application",
    supported_adapters={"~onebot.v11"},
)

EASTER_EGG_IMAGE_DIR = Path.cwd() / "src" / "asserts" / "easter_egg"


def get_easter_egg_image_path(keyword: str) -> Path:
    return EASTER_EGG_IMAGE_DIR / f"{keyword}.jpg"


caidan = on_alconna(
    Alconna("彩蛋", Args["name", str]),
    priority=1,
    block=True,
)


def find_easter_egg_keywords(text: str) -> list[str]:
    found = []
    for keyword, aliases in EASTER_EGG_KEYWORDS.items():
        for alias in aliases:
            if alias in text:
                found.append(keyword)
                break
    return found


@caidan.handle()
async def _(name: Match[str]):
    if not name.available:
        await caidan.finish("请输入角色名称，例如: 彩蛋 玲娜贝儿")
        return

    found = find_easter_egg_keywords(name.result)
    if not found:
        await caidan.finish(f"未找到匹配的彩蛋角色: {name.result}")
        return

    messages = []
    for keyword in found:
        image_path = get_easter_egg_image_path(keyword)
        if image_path.exists():
            first_alias = EASTER_EGG_KEYWORDS[keyword][0]
            messages.append(f"{first_alias}:")
            messages.append(MessageSegment.image(image_path))
        else:
            messages.append(f"{EASTER_EGG_KEYWORDS[keyword][0]}: 图片文件不存在")

    if random_text := try_load_random_text():
        messages.append(random_text)

    await caidan.finish(Message(messages))