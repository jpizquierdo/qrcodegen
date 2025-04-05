from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from app.core.config import logger


async def command_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔗 URL QR Code", callback_data="url_qr")],
        [InlineKeyboardButton("📞 Contact Info", callback_data="contact_info")],
        [InlineKeyboardButton("📶 Wi-Fi QR Code", callback_data="wifi_qr")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("🔄 Reset Command", callback_data="back")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose an option below:",
        reply_markup=reply_markup,
    )
    context.user_data.clear()


async def handle_invalid_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.debug("❌ Invalid state. Please try again.")
    await command_options(update, context)
