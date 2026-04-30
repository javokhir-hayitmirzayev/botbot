from pathlib import Path
from aiogram import F  # noqa
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile,
)
from aiogram.filters import Command
from aiogram.enums import ChatMemberStatus


from src.database.intances import user_table, pending_referrals_table
from src.bot import bot
from src.utilities.env import env
from src.utilities import logger


# Create main keyboard
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔗 Havola")],
        [KeyboardButton(text="📊 Reyting")],
        [KeyboardButton(text="🏆 Top")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)


##
##
async def handler_start_command(msg: Message, state: FSMContext):
    """Handle /start command with referral logic."""
    user_id = msg.from_user.id
    username = msg.from_user.username
    first_name = msg.from_user.first_name

    # Extract referrer_id from /start command
    referrer_id = None
    if msg.text and len(msg.text.split()) > 1:
        try:
            referrer_id = int(msg.text.split()[1])
        except (ValueError, IndexError):
            referrer_id = None

    # Check if user already exists
    if await user_table.is_user_exists(user_id):
        invite_count = await user_table.get_invite_count(user_id)
        await msg.answer(
            f"👋 Xush kelibsiz!\n\n"
            f"Siz hozirgacha {invite_count} kishini taklif qildingiz.\n\n"
            f"Quyidagi tugmalardan foydalaning:",
            reply_markup=main_keyboard
        )
        await handler_link_command(msg)
        return

    # Register user with referrer if provided
    await user_table.add_user(user_id, referrer_id, username, first_name)

    if referrer_id:
        await msg.answer(
            f"🎉 Xush kelibsiz! Siz {referrer_id} foydalanuvchisi tomonidan taklif qilindingiz.\n\n"
            f"Quyidagi tugmalardan foydalaning:",
            reply_markup=main_keyboard
        )
    else:
        await msg.answer(
            f"🎉 Taklif botiga xush kelibsiz!\n\n"
            f"Quyidagi tugmalardan foydalaning:",
            reply_markup=main_keyboard
        )

    await handler_link_command(msg)


async def handler_link_command(msg: Message):
    """Handle /link command - generate referral link."""
    user_id = msg.from_user.id
    bot_info = await bot.get_me()
    bot_username = bot_info.username

    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    promotional_text = (
        "🚀 Iqtidor Akademiyasidan\n"
        "💥 1 000 000 so'm yutib oling!\n\n"
        "Endi nafaqat bilim olasiz, balki pul ham yutib olishingiz mumkin! 💰\n\n"
        "Biz maxsus bot ishga tushirdik — u kim qancha odam qo'shganini aniq hisoblab boradi 📊\n\n"
        "🏆 Qoidalar juda oddiy:\n"
        "Bot orqali do'stlaringizni kanalga taklif qiling\n"
        "Qancha ko'p odam qo'shsangiz — imkoniyatingiz shuncha yuqori\n"
        "Eng ko'p odam qo'shgan ishtirokchi — CHEMPION!\n\n"
        "💥 Sovrinlar:\n"
        "🥇 Chempionga — 1 000 000 so'm\n\n"
        "🎁 Uni taklif qilgan odamga — 500 000 so'm\n"
        "(Chempionni taklif qilgan bo'lsangiz ham 500 ming)\n\n"
        "🔥 Bu shunchaki o'yin emas — bu real pul uchun real imkoniyat!\n"
        "⏳ Shoshiling! Har bir taklif — sizni g'alabaga yaqinlashtiradi!\n\n"
        f"🔗 Sizning taklif havolangiz:\n{referral_link}"
    )

    image_path = Path("/app/image.png")

    try:
        if image_path.exists():
            photo_file = FSInputFile(image_path)
            await msg.answer_photo(photo_file, caption=promotional_text, reply_markup=main_keyboard)
        else:
            logger.warning(f"Image file not found at {image_path}")
            await msg.answer(promotional_text, reply_markup=main_keyboard)
    except Exception as e:
        logger.error("Failed to send image: %s", e)
        await msg.answer(promotional_text, reply_markup=main_keyboard)


async def handler_link_button(msg: Message):
    """Handle '🔗 Havola' button press."""
    await handler_link_command(msg)


async def handler_rating_command(msg: Message):
    """Handle /reyting command - show user's own rating."""
    user_id = msg.from_user.id

    # Get user's invite count
    user_invite_count = await user_table.get_invite_count(user_id)

    # Get user's rank
    user_rank = await user_table.get_user_rank(user_id)

    # Get user's referrer
    user_referrer_id = await user_table.get_referrer_of_user(user_id)
    if user_referrer_id:
        referrer_info = await user_table.get_user_display_name(user_referrer_id)
    else:
        referrer_info = "Yo'q"

    # Build personal rating message
    rating_text = f"👤 Sizning statistikangiz:\n\n"
    rating_text += f"Taklif qilinganlar: {user_invite_count}\n"
    rating_text += f"Sizning o'rningiz: {user_rank}\n"
    rating_text += f"Sizi taklif qilgan: {referrer_info}"

    await msg.answer(rating_text)


async def handler_rating_button(msg: Message):
    """Handle '📊 Reyting' button press."""
    await handler_rating_command(msg)


async def handler_top_command(msg: Message):
    """Handle /top command - show top 10 referrers."""
    user_id = msg.from_user.id

    # Get top referrers
    top_referrers = await user_table.get_top_referrers(limit=10)

    # Build leaderboard message
    leaderboard_text = "🏆 Top 10 foydalanuvchilar:\n\n"
    user_in_top = False

    for idx, referrer in enumerate(top_referrers, 1):
        ref_id = referrer["referrer_id"]
        count = referrer["invite_count"]

        # Get display name for referrer
        display_name = await user_table.get_user_display_name(ref_id)

        if ref_id == user_id:
            user_in_top = True
            leaderboard_text += f"{idx}. <b>{display_name}</b> — {count} ta taklif\n"
        else:
            leaderboard_text += f"{idx}. {display_name} — {count} ta taklif\n"

    # If user is not in top 10, show their position at the end
    if not user_in_top:
        user_rank = await user_table.get_user_rank(user_id)
        user_invite_count = await user_table.get_invite_count(user_id)
        leaderboard_text += "\n...\n"
        leaderboard_text += f"{user_rank}. <b>Siz</b> — {user_invite_count} ta taklif\n"

    await msg.answer(leaderboard_text, parse_mode="HTML")


async def handler_top_button(msg: Message):
    """Handle '🏆 Top' button press."""
    await handler_top_command(msg)


async def handler_check_membership_callback(callback: CallbackQuery):
    """Handle 'Check Membership' button callback."""
    user_id = callback.from_user.id
    username = callback.from_user.username
    first_name = callback.from_user.first_name
    channel_id = env("CHANNEL_ID", None)

    if not channel_id:
        await callback.answer("⚠️ Kanal sozlanmagan", show_alert=True)
        return

    try:
        chat_member = await bot.get_chat_member(channel_id, user_id)
        status = chat_member.status

        if status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
        ):
            # Check if there's a pending referral
            pending = await pending_referrals_table.get_pending_referral(user_id)

            if pending:
                # Register the user with the referrer
                referrer_id = pending["referrer_id"]
                # Use stored data from pending referral, fallback to current data
                stored_username = pending.get("username") or username
                stored_first_name = pending.get("first_name") or first_name
                await user_table.add_user(user_id, referrer_id, stored_username, stored_first_name)
                # Delete the pending referral
                await pending_referrals_table.delete_pending_referral(user_id)
                logger.info(f"Processed pending referral: user {user_id} from referrer {referrer_id}")

                await callback.answer("✅ Siz a'zosiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.", show_alert=True)
                await callback.message.delete()
                # Send welcome message
                await bot.send_message(
                    user_id,
                    f"🎉 Botga xush kelibsiz!\n\nSizni {referrer_id} foydalanuvchisi taklif qildi.\n\nTaklif havolasini olish uchun /link va statistikangizni ko'rish uchun /reyting buyrug'ini bering!"
                )
            else:
                # No pending referral, just allow access
                await callback.answer("✅ Siz a'zosiz! Endi botdan foydalanishingiz mumkin.", show_alert=True)
                await callback.message.delete()
                # Register without referrer if not already registered
                if not await user_table.is_user_exists(user_id):
                    await user_table.add_user(user_id, None, username, first_name)
                    await bot.send_message(
                        user_id,
                        "🎉 Botga xush kelibsiz!\n\nTaklif havolasini olish uchun /link va statistikangizni ko'rish uchun /reyting buyrug'ini bering!"
                    )
        else:
            await callback.answer("❌ Siz hali a'zo emas. Avval kanalga qo'shiling.", show_alert=True)

    except Exception as e:
        logger.exception("Error checking membership in callback: %s", e)
        await callback.answer("⚠️ A'zolikni tekshirishda xatolik. Iltimos, qaytadan urinib ko'ring.", show_alert=True)
