import json

import emoji
from nonebot import (
    get_bots,
    get_driver,
    logger,
    on_command,
    on_message,
    require,
)
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule

from .face import emoji_like_id_set

require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
import nonebot_plugin_localstore as store

__plugin_meta__ = PluginMetadata(
    name="名片赞，表情回应插件",
    description="nonebot2 名片赞，表情回应插件",
    usage="赞我, 发送带表情的消息",
    type="application",
    homepage="https://github.com/fllesser/nonebot-plugin-emojilike",
    supported_adapters={"~onebot.v11"},
    extra={
        "author": "fllesser",
        "version": "0.2.0",
        "repo": "https://github.com/fllesser/nonebot-plugin-emojilike",
    },
)


def contain_face(event: GroupMessageEvent) -> bool:
    msg = event.get_message()
    return any(seg.type == "face" for seg in msg) or any(
        char in emoji.EMOJI_DATA for char in msg.extract_plain_text().strip()
    )


emojilike = on_message(rule=Rule(contain_face), permission=GROUP, block=False, priority=999)


@emojilike.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.get_message()
    msg_emoji_id_set: set[int] = {int(seg.data["id"]) for seg in msg if seg.type == "face"} | {
        ord(char) for char in msg.extract_plain_text().strip() if char in emoji.EMOJI_DATA
    }
    common_emojis = msg_emoji_id_set & emoji_like_id_set
    for emoji_id in common_emojis:
        await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id=emoji_id)


@on_command(cmd="赞我", aliases={"草我"}, permission=GROUP).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    id_set = {"76", "66", "63", "201", "10024"}
    try:
        for _ in range(5):
            await bot.send_like(user_id=event.user_id, times=10)
            await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id=id_set.pop())
    except Exception as _:
        await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id="38")


sub_like_set: set[int] = {1}
sub_list_file = "sub_list.json"


@get_driver().on_startup
async def _():
    data_file = store.get_plugin_data_file(sub_list_file)
    if not data_file.exists():
        data_file.write_text(json.dumps([]))
    global sub_like_set
    sub_like_set = set(json.loads(data_file.read_text()))
    logger.info(f"每日赞列表: [{','.join(map(str, sub_like_set))}]")


@on_command(cmd="天天赞我", aliases={"天天草我"}, permission=GROUP).handle()
async def _(bot: Bot, event: MessageEvent):
    sub_like_set.add(event.user_id)
    data_file = store.get_plugin_data_file(sub_list_file)
    data_file.write_text(json.dumps(list(sub_like_set)))
    await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id="424")


@scheduler.scheduled_job("cron", hour=8, minute=0, id="sub_card_like")
async def _():
    # 取 instance Bot
    bots = [bot for bot in get_bots().values() if isinstance(bot, Bot)]
    if not bots:
        return
    for bot in bots:
        for user_id in sub_like_set:
            try:
                for _ in range(5):
                    await bot.send_like(user_id=user_id, times=10)
            except Exception:
                continue
