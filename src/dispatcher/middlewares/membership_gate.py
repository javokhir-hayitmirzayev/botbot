from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from aiogram.enums import ChatMemberStatus

from src.bot import bot
from src.utilities.env import env
from src.utilities import logger
from src.database.intances import pending_referrals_table


class MembershipGateMiddleware(BaseMiddleware):
    """Middleware to check if user is a member of the required channel."""

    async def __call__(self, handler, event: Update, data: dict):
        # Skip membership check for non-message updates or if no channel is configured
        if not event.message or not isinstance(event.message, Message):
            return await handler(event, data)

        channel_id = env("CHANNEL_ID", None)
        if not channel_id:
            logger.warning("CHANNEL_ID not configured, skipping membership check")
            return await handler(event, data)

        # Extract referrer_id from /start command if present
        referrer_id = None
        if event.message.text and event.message.text.startswith("/start"):
            parts = event.message.text.split()
            if len(parts) > 1 and parts[1].isdigit():
                referrer_id = int(parts[1])

        try:
            chat_member = await bot.get_chat_member(channel_id, event.message.from_user.id)
            status = chat_member.status

            # Allow member, administrator, creator
            if status in (
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR,
            ):
                return await handler(event, data)

            # User is not a member - store pending referral if present
            if referrer_id:
                await pending_referrals_table.add_pending_referral(
                    event.message.from_user.id,
                    referrer_id,
                    event.message.from_user.username,
                    event.message.from_user.first_name
                )
                logger.info(f"Stored pending referral: user {event.message.from_user.id} from referrer {referrer_id}")

            # Send join message with button
            channel_url = env("CHANNEL_URL", "")
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

            if channel_url:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🔗 Kanalga qo'shiling", url=channel_url)],
                        [InlineKeyboardButton(text="✅ A'zolikni tekshiring", callback_data="check_membership")]
                    ]
                )
                await event.message.answer(
                    "⚠️ Botdan foydalanish uchun kanalimiz a'zosi bo'lishingiz shart.\n\nAvval kanalga qo'shiling, keyin 'A'zolikni tekshiring' tugmasini bosing.",
                    reply_markup=keyboard
                )
            else:
                await event.message.answer(
                    "⚠️ Botdan foydalanish uchun kanalimiz a'zosi bo'lishingiz shart.\n\nAvval kanalga qo'shiling."
                )

            return None

        except Exception as e:
            logger.exception("Error checking membership: %s", e)
            # On error, allow the request to proceed
            return await handler(event, data)
