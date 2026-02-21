from nonebot import require
from nonebot_plugin_localstore import get_plugin_data_dir, get_plugin_data_file
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.rule import to_me
from pathlib import Path
from .config import KEYWORDS, get_image_path

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Match,
    Option,
    Query,
    Subcommand,
    on_alconna,
)

dawu = on_alconna(
    Alconna(
        "大雾",
        Subcommand(
            "shiyan|sy|1",
            Args["name", str],
        )
    ),
    rule=to_me(),
    priority=0,
    block=True
)

def find_keyword(text: str) -> str | None:
    for keyword, aliases in KEYWORDS.items():
        for alias in aliases:
            if alias in text:
                return keyword
    return None

@dawu.assign("shiyan")
async def _(event: GroupMessageEvent, name: Match[str]):
    # await dawu.send(f"收到实验名称: {name.result}")
    if name.available:
        found_keyword = find_keyword(name.result)
        if found_keyword:
            image_path = get_image_path(found_keyword)
            if image_path.exists():
                await dawu.finish(MessageSegment.image(image_path), reply_message=True)
            else:
                await dawu.finish(f"找到关键词: {found_keyword}，但图片文件不存在", reply_message=True)
        else:
            await dawu.finish(f"没有在'{name.result}'中找到关键词哦，再试试呗", reply_message=True)
