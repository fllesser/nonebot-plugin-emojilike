from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageSegment
from nonebug import App
import pytest


def make_onebot_msg(message: Message) -> GroupMessageEvent:
    from time import time

    from nonebot.adapters.onebot.v11.event import Sender

    event = GroupMessageEvent(
        time=int(time()),
        sub_type="normal",
        self_id=123456,
        post_type="message",
        message_type="group",
        message_id=12345678,
        user_id=1234567890,
        group_id=1234567890,
        raw_message=message.extract_plain_text(),
        message=message,
        original_message=message,
        sender=Sender(),
        font=123456,
    )
    return event


@pytest.mark.asyncio
async def test_emojilike(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    from nonebot_plugin_emojilike import emojilike

    # only face id
    event = make_onebot_msg(
        Message("test" + MessageSegment.face(144) + "test" + MessageSegment.face(144) + "test")
    )
    async with app.test_matcher(emojilike) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": 12345678, "emoji_id": 144})
        logger.success("call api | set_msg_emoji_like emoji_id=144")
        ctx.should_finished()

    # only unicode emoji
    event = make_onebot_msg(Message("test❔❔test❔❔test"))
    async with app.test_matcher(emojilike) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": 12345678, "emoji_id": ord("❔")})
        logger.success(f"call api | set_msg_emoji_like emoji_id={ord('❔')}")
        ctx.should_finished()

    # face id 和 unicode emoji 混合
    event = make_onebot_msg(
        Message("test❔❔test❔❔test" + MessageSegment.face(144) + "test" + MessageSegment.face(144))
    )
    async with app.test_matcher(emojilike) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": 12345678, "emoji_id": 144})
        logger.success("call api | set_msg_emoji_like emoji_id=144")
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": 12345678, "emoji_id": ord("❔")})
        logger.success(f"call api | set_msg_emoji_like emoji_id={ord('❔')}")
        ctx.should_finished()
