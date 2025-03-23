from io import BytesIO
import qrcode
from pydantic import AnyUrl, EmailStr


async def generate_url_qr(url: AnyUrl) -> BytesIO:
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # level of error correction
        box_size=10,  # size of each box in pixels
        border=4,  # thickness of the border
    )
    # Add the URL data
    qr.add_data(url)
    qr.make(fit=True)
    qr = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


# Wi-Fi QR Code Generator
async def generate_wifi_qr(ssid: str, password: str) -> BytesIO:
    wifi_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr = qrcode.make(wifi_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


async def generate_contact_qr(
    name: str,
    surname: str,
    phone_number: str,
    email: EmailStr,
    company: str = "",
    title: str = "",
    url: str = "",
) -> BytesIO:
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{surname};{name};;;\nTEL;CELL:{phone_number}\nEMAIL:{email}\nORG:{company}\nTITLE:{title}\nURL:{url}\nEND:VCARD"
    qr = qrcode.make(vcard)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
