from telegram import Update
from telegram.ext import ContextTypes
from pydantic import ValidationError
from app.core.models import WifiQR,WiFiSSIDModel,UserState
from app.functions.shared import command_options
from app.qrcodegen import generate_wifi_qr

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