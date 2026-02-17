from nonebot import on_command, on_message
from nonebot.adapters import Event, Message
from nonebot.params import CommandArg, EventType

echo = on_message()


@echo.handle()
async def handle_echo(id=Event.get_user_id, type=EventType()):
    await echo.send(type)
    await echo.send(f"user id: {id}")

    await echo.send(f"message: {Event.get_message}")
