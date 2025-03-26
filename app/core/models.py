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
    AWAITING_SSID = "AWAITING_SSID"
    AWAITING_PASSWORD = "AWAITING_PASSWORD"
    AWAITING_URL = "AWAITING_URL"
    AWAITING_NAME = "AWAITING_NAME"
    AWAITING_SURNAME = "AWAITING_SURNAME"
    AWAITING_PHONE = "AWAITING_PHONE"
    AWAITING_EMAIL = "AWAITING_EMAIL"
    AWAITING_COMPANY = "AWAITING_COMPANY"
    AWAITING_TITLE = "AWAITING_TITLE"
    AWAITING_WEBSITE = "AWAITING_WEBSITE"
