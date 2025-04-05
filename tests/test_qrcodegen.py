import pytest
from app.qrcodegen import (
    generate_url_qr,
    generate_wifi_qr,
    generate_contact_qr,
    generate_text_qr,
)
from app.core.models import ContactQR, WifiQR, URLQR
from pydantic import ValidationError
from io import BytesIO


@pytest.mark.asyncio
async def test_generate_text_qr():
    qr_code = await generate_text_qr(text="blabla bleble cositas")
    assert isinstance(qr_code, BytesIO)
    assert qr_code.getvalue().startswith(b"\x89PNG")  # Check if it's a PNG file


@pytest.mark.asyncio
async def test_generate_url_qr():
    qr_code = await generate_url_qr(URLQR(url="https://example.com"))
    assert isinstance(qr_code, BytesIO)
    assert qr_code.getvalue().startswith(b"\x89PNG")  # Check if it's a PNG file


@pytest.mark.asyncio
async def test_generate_invalid_url_qr():
    with pytest.raises(ValidationError):
        await generate_url_qr(URLQR(url="invalid-url.com"))


@pytest.mark.asyncio
async def test_generate_wifi_qr():
    ssid = "TestSSID"
    password = "TestPassword"
    qr_code = await generate_wifi_qr(WifiQR(ssid=ssid, password=password))
    assert isinstance(qr_code, BytesIO)
    assert qr_code.getvalue().startswith(b"\x89PNG")  # Check if it's a PNG file


@pytest.mark.asyncio
async def test_generate_wifi_qr_ssid_too_long():
    with pytest.raises(ValidationError):
        ssid = "TestSSIDTestSSIDTestSSIDTestSSIDD"  # 33 length
        password = "TestPassword"
        await generate_wifi_qr(WifiQR(ssid=ssid, password=password))


@pytest.mark.asyncio
async def test_generate_wifi_qr_ssid_too_short():
    with pytest.raises(ValidationError):
        ssid = ""
        password = "TestPassword"
        await generate_wifi_qr(WifiQR(ssid=ssid, password=password))


@pytest.mark.asyncio
async def test_generate_wifi_qr_password_too_long():
    with pytest.raises(ValidationError):
        ssid = "TestSSID"
        password = "TestPasswordTestPasswordTestPasswordTestPasswordTestPasswordTestPasswordTestPassword"  # 84 length
        await generate_wifi_qr(WifiQR(ssid=ssid, password=password))


@pytest.mark.asyncio
async def test_generate_wifi_qr_password_too_short():
    with pytest.raises(ValidationError):
        ssid = "TestSSID"
        password = "T"
        await generate_wifi_qr(WifiQR(ssid=ssid, password=password))


@pytest.mark.asyncio
async def test_generate_contact_qr():
    qr_code = await generate_contact_qr(
        ContactQR(
            name="Joel",
            surname="Perez Izquierdo",
            phone_number="+34600312511",
            email="joelperez91@gmail.com",
            company="Example Inc.",
            title="Software Engineer",
            url="https://github.com/jpizquierdo",
        )
    )
    assert isinstance(qr_code, BytesIO)
    assert qr_code.getvalue().startswith(b"\x89PNG")  # Check if it's a PNG file


@pytest.mark.asyncio
async def test_generate_contact_qr_invalid_email():
    with pytest.raises(ValidationError):
        await generate_contact_qr(
            ContactQR(
                name="Joel",
                surname="Perez Izquierdo",
                phone_number="+34600312511",
                email="invalid-email",
            )
        )


@pytest.mark.asyncio
async def test_generate_contact_qr_invalid_url():
    with pytest.raises(ValidationError):
        await generate_contact_qr(
            ContactQR(
                name="Joel",
                surname="Perez Izquierdo",
                phone_number="+34600312511",
                email="joelperez91@gmail.com",
                url="invalid-url",
            )
        )
