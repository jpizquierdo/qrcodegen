from io import BytesIO
import qrcode

from app.core.models import ContactQR, WifiQR, URLQR


async def generate_url_qr(url: URLQR) -> BytesIO:
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # level of error correction
        box_size=10,  # size of each box in pixels
        border=4,  # thickness of the border
    )
    # Add the URL data
    qr.add_data(url.url)
    qr.make(fit=True)
    qr = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


# Wi-Fi QR Code Generator
async def generate_wifi_qr(wifi: WifiQR) -> BytesIO:
    wifi_data = f"WIFI:T:WPA;S:{wifi.ssid};P:{wifi.password};;"
    qr = qrcode.make(wifi_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


async def generate_contact_qr(contact: ContactQR) -> BytesIO:
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{contact.surname};{contact.name};;;\nTEL;CELL:{contact.phone_number}\nEMAIL:{contact.email}\nORG:{contact.company}\nTITLE:{contact.title}\nURL:{contact.url}\nEND:VCARD"
    qr = qrcode.make(vcard)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
