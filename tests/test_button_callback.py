import pytest

from unittest.mock import AsyncMock, ANY
from app.app import button_callback
from app.core.models import UserState


@pytest.mark.asyncio
async def test_button_callback_contact_info():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {}  # Use a real dictionary for user_data
    query = AsyncMock()
    query.data = "contact_info"
    update.callback_query = query
    query.message.reply_text = AsyncMock()  # Mock the async method

    # Call the button_callback function
    await button_callback(update, context)

    # Assert that the bot sends the correct message
    query.message.reply_text.assert_called_once_with("Please send the name:")
    assert context.user_data["state"] == UserState.AWAITING_NAME


@pytest.mark.asyncio
async def test_button_callback_wifi_qr():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {}  # Use a real dictionary for user_data
    query = AsyncMock()
    query.data = "wifi_qr"
    update.callback_query = query
    query.message.reply_text = AsyncMock()  # Mock the async method

    # Call the button_callback function
    await button_callback(update, context)

    # Assert that the bot sends the correct message
    query.message.reply_text.assert_called_once_with("Please send the Wi-Fi SSID:")
    assert context.user_data["state"] == UserState.AWAITING_SSID


@pytest.mark.asyncio
async def test_button_callback_url_qr():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {}  # Use a real dictionary for user_data
    query = AsyncMock()
    query.data = "url_qr"
    update.callback_query = query
    query.message.reply_text = AsyncMock()  # Mock the async method

    # Call the button_callback function
    await button_callback(update, context)

    # Assert that the bot sends the correct message
    query.message.reply_text.assert_called_once_with("Please send the URL:")
    assert context.user_data["state"] == UserState.AWAITING_URL


@pytest.mark.asyncio
async def test_button_callback_about():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {}  # Use a real dictionary for user_data
    query = AsyncMock()
    query.data = "about"
    update.callback_query = query
    query.message.reply_text = AsyncMock()  # Mock the async method

    # Call the button_callback function
    await button_callback(update, context)

    # Assert that the bot sends the correct message
    query.message.reply_text.assert_called_once_with(
        "ℹ️ This bot provides useful tools for QR codes creation:\nSuch as contact info, url, wifi, and more.\n"
        "Created with ❤️ using Python.\n\n"
        "Source code is available on GitHub: https://github.com/jpizquierdo/qrcodegen"
    )


@pytest.mark.asyncio
async def test_button_callback_back():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {}  # Use a real dictionary for user_data
    query = AsyncMock()
    query.data = "back"
    update.callback_query = query
    context.bot.send_message = AsyncMock()  # Mock the async method

    # Call the button_callback function
    await button_callback(update, context)

    # Assert that the bot sends the correct messages
    assert context.bot.send_message.call_count == 2

    # Assert the first call
    context.bot.send_message.assert_any_call(
        chat_id=update.effective_chat.id,
        text="👋 Choose and option and I'll generate a QR code for you!",
    )

    # Assert the second call (with inline keyboard)
    context.bot.send_message.assert_any_call(
        chat_id=update.effective_chat.id,
        text="Choose an option below:",
        reply_markup=ANY,  # Use ANY to match the InlineKeyboardMarkup object
    )
