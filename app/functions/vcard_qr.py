from telegram import Update
from telegram.ext import ContextTypes
from pydantic import ValidationError

from app.functions.shared import command_options
from app.qrcodegen import generate_contact_qr
from app.core.models import (
    UserState,
    EmailModel,
    ContactQR,
)


async def vcard_qr_handle_name_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["name"] = update.message.text
    context.user_data["state"] = UserState.VCARD_AWAITING_SURNAME
    await update.message.reply_text("Please send the surname:")


async def vcard_qr_handle_surname_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["surname"] = update.message.text
    context.user_data["state"] = UserState.VCARD_AWAITING_PHONE
    await update.message.reply_text("Please send the phone number with prefix:")


async def vcard_qr_handle_phone_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["phone_number"] = update.message.text
    context.user_data["state"] = UserState.VCARD_AWAITING_EMAIL
    await update.message.reply_text("Please send the email:")


async def vcard_qr_handle_email_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        email = EmailModel(email=update.message.text)  # Validation using Pydantic
        context.user_data["email"] = email.email
        context.user_data["state"] = UserState.VCARD_AWAITING_COMPANY
        await update.message.reply_text("Please send the company name:")
    except ValidationError:
        await update.message.reply_text(
            "❌ Invalid email. Please send a valid email address."
        )


async def vcard_qr_handle_company_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["company"] = update.message.text
    context.user_data["state"] = UserState.VCARD_AWAITING_TITLE
    await update.message.reply_text("Please send the job title:")


async def vcard_qr_handle_title_state(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    context.user_data["title"] = update.message.text
    context.user_data["state"] = UserState.VCARD_AWAITING_WEBSITE
    await update.message.reply_text("Please send the Website URL 🔗:")


async def vcard_qr_handle_website_state(
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
