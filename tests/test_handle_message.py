import pytest

from unittest.mock import AsyncMock, patch
from app.app import handle_message
from app.core.models import UserState, URLQR, WifiQR, ContactQR
from app.qrcodegen import generate_wifi_qr, generate_contact_qr, generate_url_qr


@pytest.mark.asyncio
async def test_handle_message_awaiting_url():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_URL}
    test_url = "https://example.com"
    update.message.text = test_url
    update.message.reply_photo = AsyncMock()  # Mock the async method

    # Mock realistic PNG-like data for the QR code
    mock_qr = await generate_url_qr(URLQR(url=test_url))
    with patch("app.qrcodegen.generate_url_qr", new=AsyncMock(return_value=mock_qr)):
        # Call the handle_message function
        await handle_message(update, context)

    # Assert by content
    assert update.message.reply_photo.call_count == 1
    actual_call = update.message.reply_photo.call_args[1]["photo"]
    assert actual_call.getvalue() == mock_qr.getvalue()

    # Optionally check the caption as well
    update.message.reply_photo.assert_called_once_with(
        photo=actual_call, caption="Here is your QR code!"
    )


@pytest.mark.asyncio
async def test_handle_message_awaiting_url_invalid():

    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_URL}
    test_url = "invalid-url.com"
    update.message.text = test_url

    await handle_message(update, context)
    assert context.user_data["state"] == UserState.AWAITING_URL
    # Assert that the bot sends an error message
    update.message.reply_text.assert_called_once_with(
        "❌ Invalid URL. Please send a valid URL starting with 'http://' or 'https://'."
    )


@pytest.mark.asyncio
async def test_handle_message_awaiting_ssid():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_SSID}
    test_ssid = "TestSSID"
    update.message.text = test_ssid
    update.message.reply_text = AsyncMock()  # Mock the async method

    # Call the handle_message function
    await handle_message(update, context)

    # Assert that the bot asks for the Wi-Fi password
    update.message.reply_text.assert_called_once_with("Please send the Wi-Fi password:")

    # Assert that the state is updated
    assert context.user_data["state"] == UserState.AWAITING_PASSWORD


@pytest.mark.asyncio
async def test_handle_message_awaiting_ssid_invalid():

    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_SSID}
    test_ssid = "TestSSIDTestSSIDTestSSIDTestSSIDTestSSIDTestSSIDTestSSIDTestSSIDTestSSIDTestSSIDTestSSIDTestSSID"
    update.message.text = test_ssid

    await handle_message(update, context)
    assert context.user_data["state"] == UserState.AWAITING_SSID
    # Assert that the bot sends an error message
    update.message.reply_text.assert_called_once_with(
        "❌ Invalid SSID. Please send a valid SSID (1-32 characters)."
    )


@pytest.mark.asyncio
async def test_handle_message_awaiting_password():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_PASSWORD, "ssid": "TestSSID"}
    test_password = "TestPassword"
    update.message.text = test_password
    update.message.reply_photo = AsyncMock()  # Mock the async method

    # Mock realistic PNG-like data for the QR code
    mock_qr = await generate_wifi_qr(WifiQR(ssid="TestSSID", password=test_password))
    with patch("app.qrcodegen.generate_wifi_qr", new=AsyncMock(return_value=mock_qr)):
        # Call the handle_message function
        await handle_message(update, context)

    # Assert by content
    actual_call = update.message.reply_photo.call_args[1]["photo"]
    assert actual_call.getvalue() == mock_qr.getvalue()
    update.message.reply_photo.assert_called_once_with(
        photo=actual_call, caption="📶 Scan to connect to Wi-Fi"
    )

    # Assert that user data is cleared
    assert context.user_data == {}
    # Assert by content
    assert update.message.reply_photo.call_count == 1


@pytest.mark.asyncio
async def test_handle_message_awaiting_password_invalid():

    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_PASSWORD, "ssid": "TestSSID"}
    test_password = "T"
    update.message.text = test_password

    await handle_message(update, context)
    assert context.user_data["state"] == UserState.AWAITING_PASSWORD
    # Assert that the bot sends an error message
    update.message.reply_text.assert_called_once_with(
        "❌ Invalid SSID or Password. Please send a valid SSID (1-32 characters) and a Valid Password between 8 and 63 characters."
    )


@pytest.mark.asyncio
async def test_handle_message_awaiting_name():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_NAME}
    test_name = "Joel"
    update.message.text = test_name
    update.message.reply_text = AsyncMock()  # Mock the async method

    # Call the handle_message function
    await handle_message(update, context)

    # Assert that the bot asks for the surname
    update.message.reply_text.assert_called_once_with("Please send the surname:")

    # Assert that the state is updated
    assert context.user_data["state"] == UserState.AWAITING_SURNAME
    assert context.user_data["name"] == test_name


@pytest.mark.asyncio
async def test_handle_message_awaiting_surname():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {"state": UserState.AWAITING_SURNAME, "name": "Joel"}
    test_surname = "Perez"
    update.message.text = test_surname
    update.message.reply_text = AsyncMock()  # Mock the async method

    # Call the handle_message function
    await handle_message(update, context)

    # Assert that the bot asks for the phone number
    update.message.reply_text.assert_called_once_with(
        "Please send the phone number with prefix:"
    )

    # Assert that the state is updated
    assert context.user_data["state"] == UserState.AWAITING_PHONE
    assert context.user_data["surname"] == test_surname


@pytest.mark.asyncio
async def test_handle_message_awaiting_phone():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {
        "state": UserState.AWAITING_PHONE,
        "name": "Joel",
        "surname": "Perez",
    }
    test_phone = "+123456789"
    update.message.text = test_phone
    update.message.reply_text = AsyncMock()  # Mock the async method

    # Call the handle_message function
    await handle_message(update, context)

    # Assert that the bot asks for the email
    update.message.reply_text.assert_called_once_with("Please send the email:")

    # Assert that the state is updated
    assert context.user_data["state"] == UserState.AWAITING_EMAIL
    assert context.user_data["phone_number"] == test_phone


@pytest.mark.asyncio
async def test_handle_message_awaiting_email():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {
        "state": UserState.AWAITING_EMAIL,
        "name": "Joel",
        "surname": "Perez",
        "phone_number": "+123456789",
    }
    test_email = "john.doe@example.com"
    update.message.text = test_email
    update.message.reply_text = AsyncMock()  # Mock the async method

    # Call the handle_message function
    await handle_message(update, context)

    # Assert that the bot asks for the company name
    update.message.reply_text.assert_called_once_with("Please send the company name:")

    # Assert that the state is updated
    assert context.user_data["state"] == UserState.AWAITING_COMPANY
    assert context.user_data["email"] == test_email


@pytest.mark.asyncio
async def test_handle_message_awaiting_email_invalid():

    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {
        "state": UserState.AWAITING_EMAIL,
        "name": "Joel",
        "surname": "Perez",
        "phone_number": "+123456789",
    }
    test_email = "joelperez91.gmail.com"
    update.message.text = test_email

    await handle_message(update, context)
    assert context.user_data["state"] == UserState.AWAITING_EMAIL
    # Assert that the bot sends an error message
    update.message.reply_text.assert_called_once_with(
        "❌ Invalid email. Please send a valid email address."
    )


@pytest.mark.asyncio
async def test_handle_message_awaiting_company():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {
        "state": UserState.AWAITING_COMPANY,
        "name": "Joel",
        "surname": "Perez",
        "phone_number": "+123456789",
        "email": "joelperez91@gmail.com",
    }
    test_company = "Example Inc."
    update.message.text = test_company
    update.message.reply_text = AsyncMock()  # Mock the async method

    # Call the handle_message function
    await handle_message(update, context)

    # Assert that the bot asks for the job title
    update.message.reply_text.assert_called_once_with("Please send the job title:")

    # Assert that the state is updated
    assert context.user_data["state"] == UserState.AWAITING_TITLE
    assert context.user_data["company"] == test_company


@pytest.mark.asyncio
async def test_handle_message_awaiting_title():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {
        "state": UserState.AWAITING_TITLE,
        "name": "Joel",
        "surname": "Perez",
        "phone_number": "+123456789",
        "email": "joelperez91@gmail.com",
        "company": "Example Inc.",
    }
    test_title = "Developer"
    update.message.text = test_title
    update.message.reply_text = AsyncMock()  # Mock the async method

    # Call the handle_message function
    await handle_message(update, context)

    # Assert that the bot asks for the website URL
    update.message.reply_text.assert_called_once_with("Please send the URL 🔗:")

    # Assert that the state is updated
    assert context.user_data["state"] == UserState.AWAITING_WEBSITE
    assert context.user_data["title"] == test_title


@pytest.mark.asyncio
async def test_handle_message_awaiting_website():
    # Mock Update and Context
    update = AsyncMock()
    context = AsyncMock()
    context.user_data = {
        "state": UserState.AWAITING_WEBSITE,
        "name": "Joel",
        "surname": "Perez",
        "phone_number": "+123456789",
        "email": "joelperez91@gmail.com",
        "company": "Example Inc.",
        "title": "Developer",
    }
    test_url = "https://example.com"
    update.message.text = test_url
    update.message.reply_photo = AsyncMock()  # Mock the async method

    # Mock realistic PNG-like data for the QR code
    mock_qr = await generate_contact_qr(
        contact=ContactQR(
            name="Joel",
            surname="Perez",
            phone_number="+123456789",
            email="joelperez91@gmail.com",
            company="Example Inc.",
            title="Developer",
            url=test_url,
        )
    )
    with patch(
        "app.qrcodegen.generate_contact_qr", new=AsyncMock(return_value=mock_qr)
    ):
        # Call the handle_message function
        await handle_message(update, context)

    # Assert by content
    assert update.message.reply_photo.call_count == 1
    actual_call = update.message.reply_photo.call_args[1]["photo"]
    assert actual_call.getvalue() == mock_qr.getvalue()
    # Assert that the bot sends the QR code
    update.message.reply_photo.assert_called_once_with(
        photo=actual_call, caption="📇 Scan to read de vcard 📞"
    )
    # Assert that user data is cleared
    assert context.user_data == {}
