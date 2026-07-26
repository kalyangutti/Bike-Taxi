import re
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import EmailStr, StringConstraints, field_validator
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel

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


class BaseModel(SQLModel):
    name: str = Field(min_length=1)
    email: EmailStr
    age: int
    phone: PhoneNumber
    password: str
    is_active: bool = True
    gender: Gender
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator("password")
    @classmethod
    def passwordchecker(cls, value) -> str:
        return validate_password(value)


class Driver(BaseModel, table=True):
    id: UUID = Field(sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True))
    vehicle_number: str
    rides: int


class User(BaseModel, table=True):
    id: UUID = Field(sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True))
