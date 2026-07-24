import re
from enum import Enum
from typing import Annotated

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


def validate_password( value) -> str:
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


class BaseClass(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    age: int = Field(ge=18)
    vehicle_number: str


class BaseDriver(BaseClass):
    password: str
    gender: Gender
    is_active: bool = Field(default=True)
    rides: int = Field(default=0, ge=0)

    @field_validator("password")
    @classmethod
    def password_validtor(cls, value) -> str:
        return validate_password(value)


class DriverRead(BaseClass):
    pass


class DriverCreate(BaseDriver):
    pass


class DriverUpdate(BaseModel):
    phone: PhoneNumber | None = None
    vehicle_number: str | None = None
 