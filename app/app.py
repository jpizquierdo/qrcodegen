import logging
from io import BytesIO

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from pydantic import ValidationError

from core.config import settings
from qrcodegen import URLModel, generate_qr_code

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 Send me a URL and I'll generate a QR code for you!",
    )


# Message handler for URL validation and QR generation
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip()
    try:
        URLModel(url=user_message)  # Validation using Pydantic
        qr_image = await generate_qr_code(user_message)
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Send QR code image
        await update.message.reply_photo(photo=buffer, caption="Here is your QR code!")
    except ValidationError:
        await update.message.reply_text(
            "❌ Invalid URL. Please send a valid URL starting with 'http://' or 'https://'."
        )
    except Exception as e:
        logging.error(f"Error generating QR code: {e}")
        await update.message.reply_text(
            "⚠️ An unexpected error occurred. Please try again."
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    start_handler = CommandHandler(command="start", callback=start)
    url_handler = MessageHandler(
        filters=filters.TEXT & ~filters.COMMAND, callback=handle_message
    )

    application.add_handler(start_handler)
    application.add_handler(url_handler)

    logging.info("🤖 Bot is running... Press Ctrl+C to stop.")
    application.run_polling()
