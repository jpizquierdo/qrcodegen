from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)
from pydantic import ValidationError

from core.config import settings, logger
from core.models import URLModel, WiFiSSIDModel, UserState, EmailModel
from qrcodegen import generate_url_qr, generate_wifi_qr, generate_contact_qr


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 Choose and option and I'll generate a QR code for you!",
    )
    await command_options(update, context)


# Message handler for QR generation
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # user_id = update.message.from_user.id
    user_state = context.user_data.get("state")

    if user_state == UserState.AWAITING_URL:
        user_message = update.message.text.strip()
        try:
            URLModel(url=user_message)  # Validation using Pydantic
            qr_code = await generate_url_qr(user_message)
            # Send QR code image
            await update.message.reply_photo(
                photo=qr_code, caption="Here is your QR code!"
            )
            # Clear user data to prevent unwanted behavior
            context.user_data.clear()
            await command_options(update, context)
        except ValidationError:
            await update.message.reply_text(
                "❌ Invalid URL. Please send a valid URL starting with 'http://' or 'https://'."
            )
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            await update.message.reply_text(
                "⚠️ An unexpected error occurred. Please try again."
            )
            context.user_data.clear()
            await command_options(update, context)
    elif user_state == UserState.AWAITING_SSID:
        try:
            WiFiSSIDModel(ssid=update.message.text)  # Validation using Pydantic
            context.user_data["ssid"] = update.message.text
            context.user_data["state"] = UserState.AWAITING_PASSWORD
            await update.message.reply_text("Please send the Wi-Fi password:")
        except ValidationError:
            await update.message.reply_text(
                "❌ Invalid SSID. Please send a valid SSID (1-32 characters)."
            )
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            await update.message.reply_text(
                "⚠️ An unexpected error occurred. Please try again."
            )
            context.user_data.clear()
            await command_options(update, context)
    elif user_state == UserState.AWAITING_PASSWORD:
        qr_code = await generate_wifi_qr(
            ssid=context.user_data["ssid"], password=update.message.text
        )
        await update.message.reply_photo(
            photo=qr_code, caption="📶 Scan to connect to Wi-Fi"
        )
        context.user_data.clear()
        await command_options(update, context)
    elif user_state == UserState.AWAITING_NAME:
        context.user_data["name"] = update.message.text
        context.user_data["state"] = UserState.AWAITING_SURNAME
        await update.message.reply_text("Please send the surname:")
    elif user_state == UserState.AWAITING_SURNAME:
        context.user_data["surname"] = update.message.text
        context.user_data["state"] = UserState.AWAITING_PHONE
        await update.message.reply_text("Please send the phone number with prefix:")
    elif user_state == UserState.AWAITING_PHONE:
        context.user_data["phone_number"] = update.message.text
        context.user_data["state"] = UserState.AWAITING_EMAIL
        await update.message.reply_text("Please send the email:")
    elif user_state == UserState.AWAITING_EMAIL:
        try:
            EmailModel(email=update.message.text)  # Validation using Pydantic
            context.user_data["email"] = update.message.text
            context.user_data["state"] = UserState.AWAITING_COMPANY
            await update.message.reply_text("Please send the company:")
        except ValidationError:
            await update.message.reply_text(
                "❌ Invalid email. Please send a valid email address."
            )
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            await update.message.reply_text(
                "⚠️ An unexpected error occurred. Please try again."
            )
            context.user_data.clear()
            await command_options(update, context)
    elif user_state == UserState.AWAITING_COMPANY:
        context.user_data["company"] = update.message.text
        context.user_data["state"] = UserState.AWAITING_TITLE
        await update.message.reply_text("Please send the job title:")
    elif user_state == UserState.AWAITING_TITLE:
        context.user_data["title"] = update.message.text
        context.user_data["state"] = UserState.AWAITING_WEBSITE
        await update.message.reply_text("Please send the URL 🔗:")
    elif user_state == UserState.AWAITING_WEBSITE:
        url = update.message.text.strip()
        qr_code = await generate_contact_qr(
            name=context.user_data["name"],
            surname=context.user_data["surname"],
            phone_number=context.user_data["phone_number"],
            email=context.user_data["email"],
            company=context.user_data["company"],
            title=context.user_data["title"],
            url=url,
        )
        await update.message.reply_photo(
            photo=qr_code, caption="📇 Scan to read de vcard 📞"
        )
        context.user_data.clear()
        await command_options(update, context)

    else:
        await command_options(update, context)


# Addtional Menu
async def command_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔗 URL QR Code", callback_data="url_qr")],
        [InlineKeyboardButton("📞 Contact Info", callback_data="contact_info")],
        [InlineKeyboardButton("📶 Wi-Fi QR Code", callback_data="wifi_qr")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("🔄 Reset Command", callback_data="back")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # await update.message.reply_text(
    #     "Choose an option below:", reply_markup=reply_markup
    # )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose an option below:",
        reply_markup=reply_markup,
    )
    context.user_data.clear()


# Handle Button Callbacks
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "contact_info":
        await query.message.reply_text("Please send the name:")
        context.user_data["state"] = UserState.AWAITING_NAME
    elif query.data == "wifi_qr":
        await query.message.reply_text("Please send the Wi-Fi SSID:")
        context.user_data["state"] = UserState.AWAITING_SSID
    elif query.data == "url_qr":
        await query.message.reply_text("Please send the URL:")
        context.user_data["state"] = UserState.AWAITING_URL
    elif query.data == "about":
        await query.message.reply_text(
            "ℹ️ This bot provides useful tools for QR codes creation:\nSuch as contact info, url, wifi, and more.\n"
            "Created with ❤️ using Python.\n\n"
            "Source code is available on GitHub: https://github.com/jpizquierdo/qrcodegen"
        )

    elif query.data == "back":
        await start(update, context)


if __name__ == "__main__":
    application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    start_handler = CommandHandler(command="start", callback=start)
    command_options_handler = CommandHandler(command="more", callback=command_options)
    url_handler = MessageHandler(
        filters=filters.TEXT & ~filters.COMMAND, callback=handle_message
    )
    button_query_handler = CallbackQueryHandler(button_callback)

    application.add_handler(start_handler)
    application.add_handler(url_handler)
    application.add_handler(command_options_handler)
    application.add_handler(button_query_handler)

    logger.info("🤖 Bot is running... Press Ctrl+C to stop.")
    application.run_polling()
