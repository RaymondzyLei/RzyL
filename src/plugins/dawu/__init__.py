from nonebot import require
from nonebot_plugin_localstore import get_plugin_data_dir, get_plugin_data_file
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.rule import to_me, Rule
from nonebot.adapters.onebot.v11 import Bot
from pathlib import Path
from .config import KEYWORDS, get_image_path, ALLOWED_GROUPS
from .ai_match import ai_match

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

def check_group(event: GroupMessageEvent) -> bool:
    if not ALLOWED_GROUPS:
        return True
    return event.group_id in ALLOWED_GROUPS

dawu1 = on_alconna(
    Alconna(
        "大雾1",
        Args["name", str]
    ),
    rule=Rule(check_group),
    #rule=to_me(),
    priority=0,
    block=True
)

def find_keywords(text: str) -> list[str]:
    found_keywords = []
    for keyword, aliases in KEYWORDS.items():
        for alias in aliases:
            if alias in text:
                found_keywords.append(keyword)
                break
    return found_keywords

async def send_keyword_images(keywords: list[str], prefix: str = "找到关键词"):
    messages = []
    missing_keywords = []
    for keyword in keywords:
        if keyword in KEYWORDS:
            image_path = get_image_path(keyword)
            if image_path.exists():
                first_alias = KEYWORDS[keyword][0] if KEYWORDS[keyword] else keyword
                messages.append(f"{prefix}: {first_alias}:")
                messages.append(MessageSegment.image(image_path))
            else:
                missing_keywords.append(keyword)
    
    if messages:
        if missing_keywords:
            messages.append(f"{prefix}: {', '.join(keywords)}，但部分图片文件不存在: {', '.join(missing_keywords)}")
        await dawu1.finish(messages, reply_message=True)
    else:
        await dawu1.finish(f"{prefix}: {', '.join(keywords)}，但所有图片文件都不存在", reply_message=True)

@dawu1.handle()
async def _(event: GroupMessageEvent, name: Match[str]): #event: GroupMessageEvent在Console调试的时候要删掉
    #await dawu1.send(f"群号: {event.group_id}")
    if name.available:
        if name.result == "ls":
            output_lines = []
            for keyword, aliases in KEYWORDS.items():
                output_lines.append(", ".join(aliases))
            await dawu1.finish("\n".join(output_lines), reply_message=True)
        if name.result == "help":
            await dawu1.finish("使用方法: 大雾1 实验名称\n例如: 大雾1 杨氏模量\n\n如果有多个关键词匹配，会显示所有匹配的关键词和对应的图片。\n如果有关键词匹配但图片不存在，会显示缺失的图片文件名。\n如果没有匹配的关键词，会提示没有找到关键词。", reply_message=True)
        else:
            found_keywords = find_keywords(name.result)
            if found_keywords:
                await send_keyword_images(found_keywords)
            else:
                await dawu1.send(f"没有在'{name.result}'中找到关键词哦，正在尝试AI模糊匹配...", reply_message=True)
                ai_keywords = await ai_match(name.result, KEYWORDS)
                
                if ai_keywords:
                    await send_keyword_images(ai_keywords, "AI匹配到关键词")
                else:
                    await dawu1.finish(f"AI也没有找到匹配的关键词，请使用'大雾1 ls'查看所有关键词", reply_message=True)
