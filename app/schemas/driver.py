import re
from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, StringConstraints, field_validator


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


PhoneNumber = Annotated[
    str,
    StringConstraints(
        pattern=r"^[6-9]\d{9}$",
        strip_whitespace=True,
    ),
]


def validate_password(value) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit.")

    if not re.search(r"[!@#$%^&*()~{}\[\]\";<>?/]", value):
        raise ValueError("Password must contain at least one special character.")

    return value


def validate_license(value) -> str:
    value = value.strip().upper()

    if len(value) < 5:
        raise ValueError("License Number must be at least 5 Characters long..")

    if len(value) > 20:
        raise ValueError("License number must be not exceed 20 Characters.")

    if not re.fullmatch(r"[A-Z0-9-]+", value):
        raise ValueError("License Number can contain only letters,numbers and hypens.")
    return value


class BaseClass(BaseModel):
    name: str
    email: EmailStr
    gender: Gender
    phone: PhoneNumber
    age: int = Field(ge=18)
    license_number: str

    @field_validator("license_number")
    @classmethod
    def license_validator(cls, value: str) -> str:
        return validate_license(value)


class BaseDriver(BaseClass):
    password: str

    current_latitude: float | None = None
    current_longitude: float | None = None

    total_rides: int = Field(default=0, ge=0)

    @field_validator("password")
    @classmethod
    def password_validator(cls, value: str) -> str:
        return validate_password(value)


class DriverRead(BaseClass):
    pass


class DriverCreate(BaseDriver):
    pass


class DriverUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: Gender | None = None


class DriverRespone(BaseModel):
    id: UUID
    name: str
    age: int = Field(ge=18)

    gender: Gender
    is_active: bool = Field(default=True)
    rides: int = Field(default=0, ge=0)


class ChangePassword(BaseModel):
    old_password: str
    new_password: str

    @field_validator("old_password", "new_password")
    @classmethod
    def validate_password_fields(cls, value: str) -> str:
        return validate_password(value)
