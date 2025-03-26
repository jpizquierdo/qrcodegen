import pytest

from unittest.mock import AsyncMock, patch
from app.app import start


@pytest.mark.asyncio
async def test_start():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.bot.send_message = AsyncMock()  # Mock the async method
    update.effective_chat.id = 12345

    # Mock command_options to prevent additional calls
    with patch("app.app.command_options", new=AsyncMock()):
        # Call the start function
        await start(update, context)

    # Assert that the bot sends the correct message
    context.bot.send_message.assert_called_once_with(
        chat_id=12345,
        text="👋 Choose and option and I'll generate a QR code for you!",
    )
