import json
import emoji

from nonebot import logger, require, on_command, on_message, get_driver, get_bots
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
from nonebot.adapters import Bot as BaseBot
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
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
    supported_adapters={ "~onebot.v11" }
)


def contain_face(event: GroupMessageEvent) -> bool:
    msg = event.get_message()
    return (
        any(seg.type == 'face' for seg in msg) or
        any(char in emoji.EMOJI_DATA for char in msg.extract_plain_text().strip())
    )

emojilike = on_message(rule=Rule(contain_face), permission=GROUP)
cardlike = on_command(cmd="赞我", permission=GROUP)
sub_card_like = on_command(cmd="天天赞我", permission=GROUP)

@emojilike.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.get_message()
    msg_emoji_id_set: set[int] = {
        int(seg.data.get('id')) for seg in msg if seg.type == "face"} | {ord(char) for char in msg.extract_plain_text().strip() if char in emoji.EMOJI_DATA
        }
    for id in msg_emoji_id_set:
        if id in emoji_like_id_set:
            await bot.call_api("set_msg_emoji_like", message_id = event.message_id, emoji_id = id)

@cardlike.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    id_set = {'76', '66', '63', '201', '10024'}
    try:
        for _ in range(5):
            await bot.send_like(user_id = event.get_user_id(), times = 10)
            await bot.call_api("set_msg_emoji_like", message_id = event.message_id, emoji_id = id_set.pop())
    except Exception as _:
        await bot.call_api("set_msg_emoji_like", message_id = event.message_id, emoji_id = '38')


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

@sub_card_like.handle()
async def _(bot: Bot, event: MessageEvent):
    sub_like_set.add(event.user_id)
    data_file = store.get_plugin_data_file(sub_list_file)
    data_file.write_text(json.dumps(list(sub_like_set)))
    await bot.call_api("set_msg_emoji_like", message_id = event.message_id, emoji_id = '424')


@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=0,
)
async def _():
    bots: dict[str, BaseBot] = get_bots()
    if not bots or len(bots) == 0:
        return
    for _, bot in bots:
        if isinstance(bot, Bot):
            for user_id in sub_like_set:
                try:
                    for _ in range(5):
                        await bot.send_like(user_id = user_id, times = 10)
                except Exception as _:
                    continue