import sys
import os

# to be able to import from app.*, as a package and not as a module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)
from app.core.config import settings, logger, logfire
from app.core.models import (
    UserState,
)
from app.functions.text_qr import text_qr_handle_text_state
from app.functions.url_qr import url_qr_handle_url_state, svg_url_qr_handle_url_state
from app.functions.wifi_qr import (
    wifi_qr_handle_ssid_state,
    wifi_qr_handle_password_state,
)
from app.functions.vcard_qr import (
    vcard_qr_handle_name_state,
    vcard_qr_handle_surname_state,
    vcard_qr_handle_phone_state,
    vcard_qr_handle_email_state,
    vcard_qr_handle_company_state,
    vcard_qr_handle_title_state,
    vcard_qr_handle_website_state,
)
from app.functions.shared import command_options, handle_invalid_state


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
        UserState.TEXT_AWAITING_TEXT: text_qr_handle_text_state,
        UserState.URL_AWAITING_URL: url_qr_handle_url_state,
        UserState.SVG_URL_AWAITING_URL: svg_url_qr_handle_url_state,
        UserState.WIFI_AWAITING_SSID: wifi_qr_handle_ssid_state,
        UserState.WIFI_AWAITING_PASSWORD: wifi_qr_handle_password_state,
        UserState.VCARD_AWAITING_NAME: vcard_qr_handle_name_state,
        UserState.VCARD_AWAITING_SURNAME: vcard_qr_handle_surname_state,
        UserState.VCARD_AWAITING_PHONE: vcard_qr_handle_phone_state,
        UserState.VCARD_AWAITING_EMAIL: vcard_qr_handle_email_state,
        UserState.VCARD_AWAITING_COMPANY: vcard_qr_handle_company_state,
        UserState.VCARD_AWAITING_TITLE: vcard_qr_handle_title_state,
        UserState.VCARD_AWAITING_WEBSITE: vcard_qr_handle_website_state,
    }

    # Call the appropriate handler or fallback
    handler = state_handlers.get(user_state, handle_invalid_state)
    with logfire.span(str(handler.__name__)):
        await handler(update, context)


# Handle Button Callbacks
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "contact_info":
        await query.message.reply_text("Please send the name:")
        context.user_data["state"] = UserState.VCARD_AWAITING_NAME
    elif query.data == "wifi_qr":
        await query.message.reply_text("Please send the Wi-Fi SSID:")
        context.user_data["state"] = UserState.WIFI_AWAITING_SSID
    elif query.data == "url_qr":
        await query.message.reply_text("Please send the URL:")
        context.user_data["state"] = UserState.URL_AWAITING_URL
    elif query.data == "svg_url_qr":
        await query.message.reply_text("Please send the URL:")
        context.user_data["state"] = UserState.SVG_URL_AWAITING_URL
    elif query.data == "about":
        await query.message.reply_text(
            "ℹ️ This bot provides useful tools for QR codes creation:\nSuch as contact info, url, wifi, and more.\n"
            "Created with ❤️ using Python.\n\n"
            "Source code is available on GitHub: https://github.com/jpizquierdo/qrcodegen"
        )
    elif query.data == "back":
        await start(update, context)
    elif query.data == "text_qr":
        await query.message.reply_text("Please send the text:")
        context.user_data["state"] = UserState.TEXT_AWAITING_TEXT


if __name__ == "__main__":  # pragma: no cover
    application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    start_handler = CommandHandler(command="start", callback=start)
    command_options_handler = CommandHandler(command="more", callback=command_options)
    msg_handler = MessageHandler(
        filters=filters.TEXT & ~filters.COMMAND, callback=handle_message
    )
    button_query_handler = CallbackQueryHandler(button_callback)

    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    application.add_handler(command_options_handler)
    application.add_handler(button_query_handler)

    logger.info("🤖 Bot is running... Press Ctrl+C to stop.")
    application.run_polling()
