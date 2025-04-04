import sys
import os

# to be able to import from app.*, as a package and not as a module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
from app.core.config import settings, logger
from app.core.models import (
    URLQR,
    WiFiSSIDModel,
    UserState,
    EmailModel,
    WifiQR,
    ContactQR,
)
from app.qrcodegen import generate_url_qr, generate_wifi_qr, generate_contact_qr


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 Choose and option and I'll generate a QR code for you!",
    )
    await command_options(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_state = context.user_data.get("state")

    # Mapping states to their respective handlers
    state_handlers = {
        UserState.AWAITING_URL: handle_url_state,
        UserState.AWAITING_SSID: handle_ssid_state,
        UserState.AWAITING_PASSWORD: handle_password_state,
        UserState.AWAITING_NAME: handle_name_state,
        UserState.AWAITING_SURNAME: handle_surname_state,
        UserState.AWAITING_PHONE: handle_phone_state,
        UserState.AWAITING_EMAIL: handle_email_state,
        UserState.AWAITING_COMPANY: handle_company_state,
        UserState.AWAITING_TITLE: handle_title_state,
        UserState.AWAITING_WEBSITE: handle_website_state,
    }

    # Call the appropriate handler or fallback
    handler = state_handlers.get(user_state, handle_invalid_state)
    await handler(update, context)


async def handle_url_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        qr_code = await generate_url_qr(URLQR(url=update.message.text.strip()))
        # Send QR code image
        await update.message.reply_photo(photo=qr_code, caption="Here is your QR code!")
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


async def handle_ssid_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        wifi = WiFiSSIDModel(ssid=update.message.text)  # Validation using Pydantic
        context.user_data["ssid"] = wifi.ssid
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


async def handle_password_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        qr_code = await generate_wifi_qr(
            WifiQR(ssid=context.user_data["ssid"], password=update.message.text)
        )
        await update.message.reply_photo(
            photo=qr_code, caption="📶 Scan to connect to Wi-Fi"
        )
        context.user_data.clear()
        await command_options(update, context)
    except ValidationError:
        await update.message.reply_text(
            "❌ Invalid SSID or Password. Please send a valid SSID (1-32 characters) and a Valid Password between 8 and 63 characters."
        )


async def handle_name_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["name"] = update.message.text
    context.user_data["state"] = UserState.AWAITING_SURNAME
    await update.message.reply_text("Please send the surname:")


async def handle_surname_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["surname"] = update.message.text
    context.user_data["state"] = UserState.AWAITING_PHONE
    await update.message.reply_text("Please send the phone number with prefix:")


async def handle_phone_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["phone_number"] = update.message.text
    context.user_data["state"] = UserState.AWAITING_EMAIL
    await update.message.reply_text("Please send the email:")


async def handle_email_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        email = EmailModel(email=update.message.text)  # Validation using Pydantic
        context.user_data["email"] = email.email
        context.user_data["state"] = UserState.AWAITING_COMPANY
        await update.message.reply_text("Please send the company name:")
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


async def handle_company_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["company"] = update.message.text
    context.user_data["state"] = UserState.AWAITING_TITLE
    await update.message.reply_text("Please send the job title:")


async def handle_title_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["title"] = update.message.text
    context.user_data["state"] = UserState.AWAITING_WEBSITE
    await update.message.reply_text("Please send the Website URL 🔗:")


async def handle_website_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        qr_code = await generate_contact_qr(
            ContactQR(
                name=context.user_data["name"],
                surname=context.user_data["surname"],
                phone_number=context.user_data["phone_number"],
                email=context.user_data["email"],
                company=context.user_data["company"],
                title=context.user_data["title"],
                url=update.message.text.strip(),
            )
        )
    except ValidationError:
        await update.message.reply_text(
            "❌ Invalid URL. Please send a valid URL starting with 'http://' or 'https://'."
        )
        return None

    await update.message.reply_photo(
        photo=qr_code, caption="📇 Scan to read de vcard 📞"
    )
    context.user_data.clear()
    await command_options(update, context)


async def handle_invalid_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.debug("❌ Invalid state. Please try again.")
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


if __name__ == "__main__":  # pragma: no cover
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
