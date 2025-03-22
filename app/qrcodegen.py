import qrcode
from PIL import Image
from pydantic import BaseModel, HttpUrl


class URLModel(BaseModel):
    url: HttpUrl


async def generate_qr_code(url: HttpUrl) -> Image:
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
    qr_image = qr.make_image(fill="black", back_color="white")

    return qr_image
