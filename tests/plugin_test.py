from fake import fake_group_message_event_v11
import nonebot
from nonebot import logger
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebug import App
import pytest


@pytest.mark.asyncio
async def test_emojilike(app: App):
    from nonebot_plugin_emojilike import emojilike

    # only face id
    event = fake_group_message_event_v11(
        message=Message("test" + MessageSegment.face(144) + "test" + MessageSegment.face(144) + "test")
    )
    async with app.test_matcher(emojilike) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": event.message_id, "emoji_id": 144})
        logger.success(f"reaction emoji 144 | {event.message.to_rich_text()}")
        ctx.should_finished()

    # only unicode emoji
    event = fake_group_message_event_v11(message=Message("test❔❔test❔❔test"))
    async with app.test_matcher(emojilike) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": event.message_id, "emoji_id": ord("❔")})
        logger.success(f"reaction emoji {ord('❔')} | {event.message.to_rich_text()}")
        ctx.should_finished()

    # face id 和 unicode emoji 混合
    event = fake_group_message_event_v11(
        message=Message("test❔❔test❔❔test" + MessageSegment.face(144) + "test" + MessageSegment.face(144))
    )
    async with app.test_matcher(emojilike) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": event.message_id, "emoji_id": 144})
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": event.message_id, "emoji_id": ord("❔")})
        logger.success(f"reaction emoji 144, {ord('❔')} | {event.message.to_rich_text()}")
        ctx.should_finished()


@pytest.mark.asyncio
async def test_like_me(app: App):
    event = fake_group_message_event_v11(message="赞我")
    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        id_set = {"76", "66", "63", "201", "10024"}
        for _ in range(5):
            ctx.should_call_api("send_like", data={"user_id": event.user_id, "times": 10})
            ctx.should_call_api("set_msg_emoji_like", data={"message_id": event.message_id, "emoji_id": id_set.pop()})
        ctx.should_finished()


@pytest.mark.asyncio
async def test_sub_like_me(app: App):
    event = fake_group_message_event_v11(message="天天赞我")

    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_api("set_msg_emoji_like", data={"message_id": event.message_id, "emoji_id": "424"})

    from nonebot_plugin_emojilike import SUB_LIKE_SET

    assert event.user_id in SUB_LIKE_SET
