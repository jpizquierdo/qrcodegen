from telegram import Update
from telegram.ext import ContextTypes
from pydantic import ValidationError
from app.core.models import URLQR
from app.functions.shared import command_options
from app.qrcodegen import generate_url_qr


async def url_qr_handle_url_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
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


async def svg_url_qr_handle_url_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        qr_code = await generate_url_qr(
            URLQR(url=update.message.text.strip()), svg=True
        )
        # Send QR code image
        await update.message.reply_document(
            document=qr_code, caption="Here is your QR code!"
        )
        # Clear user data to prevent unwanted behavior
        context.user_data.clear()
        await command_options(update, context)
    except ValidationError:
        await update.message.reply_text(
            "❌ Invalid URL. Please send a valid URL starting with 'http://' or 'https://'."
        )
