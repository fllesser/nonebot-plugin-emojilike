import json
from typing import Literal

import emoji
from nonebot import get_bots, get_driver, require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.log import logger
from nonebot.plugin import PluginMetadata, on_message, on_startswith
from nonebot.rule import Rule

from .face import EMOJI_LIKE_ID_SET

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
        "version": "0.2.3",
        "repo": "https://github.com/fllesser/nonebot-plugin-emojilike",
    },
)


def contain_emoji(event: GroupMessageEvent) -> bool:
    msg = event.get_message()
    return msg.has("face") or any(char in emoji.EMOJI_DATA for char in msg.extract_plain_text().strip())


emojilike = on_message(rule=Rule(contain_emoji), permission=GROUP, block=False, priority=999)


@emojilike.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.get_message()
    emoji_ids_in_msg = {int(seg.data["id"]) for seg in msg["face"]} | {
        ord(char) for char in msg.extract_plain_text().strip() if char in emoji.EMOJI_DATA
    }
    for emoji_id in emoji_ids_in_msg & EMOJI_LIKE_ID_SET:
        await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id=emoji_id)


@on_startswith(msg=("赞我", "草我"), permission=GROUP).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    id_set = {"76", "66", "63", "201", "10024"}
    try:
        for _ in range(5):
            await bot.send_like(user_id=event.user_id, times=10)
            await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id=id_set.pop())
    except Exception:
        await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id="38")


# 每日赞列表
SUB_LIKE_SET: set[int] = set()
# 每日赞列表文件名
SUB_LIST_FILE: Literal["sub_list.json"] = "sub_list.json"


@get_driver().on_startup
async def _():
    """初始化每日赞列表"""
    data_file = store.get_plugin_data_file(SUB_LIST_FILE)
    if not data_file.exists():
        data_file.write_text(json.dumps([]))
    global SUB_LIKE_SET
    SUB_LIKE_SET = set(json.loads(data_file.read_text()))
    logger.info(f"每日赞列表: [{','.join(map(str, SUB_LIKE_SET))}]")


@on_startswith(msg=("天天赞我", "天天草我"), permission=GROUP).handle()
async def _(bot: Bot, event: MessageEvent):
    SUB_LIKE_SET.add(event.user_id)
    data_file = store.get_plugin_data_file(SUB_LIST_FILE)
    data_file.write_text(json.dumps(list(SUB_LIKE_SET)))
    await bot.call_api("set_msg_emoji_like", message_id=event.message_id, emoji_id="424")


@scheduler.scheduled_job("cron", hour=8, minute=0, id="sub_card_like")
async def _():
    # 取 instance Bot
    bots = [bot for bot in get_bots().values() if isinstance(bot, Bot)]
    if not bots:
        return
    for bot in bots:
        for user_id in SUB_LIKE_SET:
            try:
                for _ in range(5):
                    await bot.send_like(user_id=user_id, times=10)
            except Exception:
                continue
