from telegram import Update
from telegram.ext import ContextTypes
from app.functions.shared import command_options
from app.qrcodegen import generate_text_qr


async def text_qr_handle_text_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    qr_code = await generate_text_qr(text=update.message.text)
    # Send QR code image
    await update.message.reply_photo(photo=qr_code, caption="Here is your QR code!")
    # Clear user data to prevent unwanted behavior
    context.user_data.clear()
    await command_options(update, context)
