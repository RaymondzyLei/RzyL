import logging
import random
import time
from collections import defaultdict
from pathlib import Path

import aiohttp
from nonebot import require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment, Message
from nonebot.rule import Rule, to_me
from nonebot.rule import Rule, to_me
from nonebot_plugin_localstore import get_plugin_data_dir, get_plugin_data_file

from .ai_match import ai_match
from .config import ALLOWED_GROUPS, KEYWORDS, get_image_path

logger = logging.getLogger(__name__)

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

RATE_LIMIT = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 10


def check_rate_limit(user_id: int) -> bool:
    now = time.time()
    user_requests = RATE_LIMIT[user_id]
    user_requests = [t for t in user_requests if now - t < 60]
    RATE_LIMIT[user_id] = user_requests
    return len(user_requests) < MAX_REQUESTS_PER_MINUTE


def validate_input(text: str) -> bool:
    if not text or not text.strip():
        return False
    if len(text) > 100:
        return False
    return True


def check_group(event: GroupMessageEvent) -> bool:
    if not ALLOWED_GROUPS:
        return True
    return event.group_id in ALLOWED_GROUPS


dawu1 = on_alconna(
    Alconna("大雾1", Args["name", str]),
    rule=Rule(check_group),
    # rule=to_me(),
    priority=0,
    block=True,
)


def find_keywords(text: str) -> list[str]:
    found_keywords = []
    for keyword, aliases in KEYWORDS.items():
        for alias in aliases:
            if alias in text:
                found_keywords.append(keyword)
                break
    return found_keywords


async def send_keyword_images(keywords: list[str], prefix: str = ""):
    
    messages = []
    missing_keywords = []
    for keyword in keywords:
        if keyword in KEYWORDS:
            image_path = get_image_path(keyword)
            if image_path.exists():
                first_alias = KEYWORDS[keyword][0] if KEYWORDS[keyword] else keyword
                messages.append(f"{prefix}{first_alias}:")
                messages.append(MessageSegment.image(image_path))
            else:
                missing_keywords.append(keyword)

    if messages:
        if missing_keywords:
            messages.append(
                f"{prefix}: {', '.join(keywords)}，但部分图片文件不存在: {', '.join(missing_keywords)}"
            )
        if random.random() < 0.05:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://v1.hitokoto.cn/?encode=text") as resp:
                        hitokoto = await resp.text()
                        if hitokoto:
                            messages.append(f"\n{hitokoto}")
            except Exception:
                pass
        await dawu1.finish(Message(messages))
    else:
        await dawu1.finish(f"{prefix}: {', '.join(keywords)}，但所有图片文件都不存在")


@dawu1.handle()
async def _(
    event: GroupMessageEvent, name: Match[str]
):  # event: GroupMessageEvent在Console调试的时候要删掉
    logger.info(f"收到请求: 群{event.group_id}, 用户{event.user_id}, 内容{name.result}")

    if not name.available:
        return

    if not validate_input(name.result):
        await dawu1.finish("输入无效，请提供有效的实验名称（1-100个字符）")
        return

    if not check_rate_limit(event.user_id):
        await dawu1.finish("请求过于频繁，请稍后再试（每分钟最多10次请求）")
        return

    if name.result == "ls":
        output_lines = []
        for keyword, aliases in KEYWORDS.items():
            output_lines.append(", ".join(aliases))
        await dawu1.finish("\n".join(output_lines))
    elif name.result == "help":
        await dawu1.finish(
            "使用方法: 大雾1 实验名称\n例如: 大雾1 杨氏模量\n\n如果有多个关键词匹配，会显示所有匹配的关键词和对应的图片。\n如果有关键词匹配但图片不存在，会显示缺失的图片文件名。\n如果没有匹配的关键词，会提示没有找到关键词。",
            reply_message=True,
        )
    else:
        found_keywords = find_keywords(name.result)
        if found_keywords:
            await send_keyword_images(found_keywords)
        else:
            await dawu1.send(
                f"没有在'{name.result}'中找到关键词哦，正在尝试AI模糊匹配..."
            )
            ai_keywords = await ai_match(name.result, KEYWORDS)

            if ai_keywords:
                await send_keyword_images(ai_keywords, "AI匹配到关键词： ")
            else:
                await dawu1.finish(
                    f"AI也没有找到匹配的关键词，请使用'大雾1 ls'查看所有关键词"
                )
