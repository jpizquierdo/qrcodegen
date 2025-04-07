from enum import StrEnum, unique
from pydantic import BaseModel, AnyUrl, Field, EmailStr


class URLQR(BaseModel):
    url: AnyUrl


class WiFiSSIDModel(BaseModel):
    ssid: str = Field(min_length=1, max_length=32)


class WifiQR(WiFiSSIDModel):
    password: str = Field(min_length=8, max_length=63)


class EmailModel(BaseModel):
    email: EmailStr


class ContactQR(EmailModel):
    name: str
    surname: str
    phone_number: str
    company: str | None = ""
    title: str | None = ""
    url: AnyUrl | None = ""


# States for user interactions
@unique
class UserState(StrEnum):
    WIFI_AWAITING_SSID = "WIFI_AWAITING_SSID"
    WIFI_AWAITING_PASSWORD = "WIFI_AWAITING_PASSWORD"
    URL_AWAITING_URL = "URL_AWAITING_URL"
    SVG_URL_AWAITING_URL = "SVG_URL_AWAITING_URL"
    VCARD_AWAITING_NAME = "VCARD_AWAITING_NAME"
    VCARD_AWAITING_SURNAME = "VCARD_AWAITING_SURNAME"
    VCARD_AWAITING_PHONE = "VCARD_AWAITING_PHONE"
    VCARD_AWAITING_EMAIL = "VCARD_AWAITING_EMAIL"
    VCARD_AWAITING_COMPANY = "VCARD_AWAITING_COMPANY"
    VCARD_AWAITING_TITLE = "VCARD_AWAITING_TITLE"
    VCARD_AWAITING_WEBSITE = "VCARD_AWAITING_WEBSITE"
    TEXT_AWAITING_TEXT = "TEXT_AWAITING_TEXT"
