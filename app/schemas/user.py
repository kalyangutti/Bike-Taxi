import re
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, StringConstraints, field_validator

PhoneNumber = Annotated[
    str, StringConstraints(pattern=r"^[6-9]\d{9}$", strip_whitespace=True)
]


def validate_password(value) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 Characters long.")

    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contains at least one upperCase letter.")

    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contains at least one lowerCase letter.")

    if not re.search(r"\d", value):
        raise ValueError("Password must contians at one digit.")

    if not re.search(r"""[!@#$%^&*(){}\[\]" ?/<>,.\-:]""", value):
        raise ValueError("Password must contian one special character")

    return value


class Gender(str, Enum):
    male = "MALE"
    female = "FEMALE"


class BaseUser(BaseModel):
    name: str
    age: int
    email: EmailStr
    phone: PhoneNumber
    gender: Gender


class UserRead(BaseUser):
    id: UUID
    pass


class UserCreate(BaseUser):
    password: str

    @field_validator("password")
    @classmethod
    def password_validator(cls, value) -> str:
        return validate_password(value)


class UserDetailsUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: PhoneNumber | None = None
    age: int | None = None
    gender: Gender | None = None


class UserRespone(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    age: int
    gender: Gender
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str

    @field_validator("old_password", "new_password")
    @classmethod
    def validate_password_fields(cls, value: str) -> str:
        return validate_password(value)
