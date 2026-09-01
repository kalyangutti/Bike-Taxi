import re
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID, uuid4

from pydantic import EmailStr, StringConstraints, field_validator
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, Relationship, SQLModel

PhoneNumber = Annotated[
    str,
    StringConstraints(
        pattern=r"^[6-9]\d{9}$",
        strip_whitespace=True,
    ),
]


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 Characters long.")

    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit.")

    if not re.search(r"""[!@#$%^&*(){}\[\]" ?/<>,.\-:]""", value):
        raise ValueError("Password must contain one special character.")

    return value


def validate_license(value: str) -> str:
    value = value.strip().upper()

    if len(value) < 5:
        raise ValueError("License Number must be at least 5 characters long.")

    if len(value) > 20:
        raise ValueError("License number must not exceed 20 characters.")

    if not re.fullmatch(r"[A-Z0-9-]+", value):
        raise ValueError(
            "License Number can contain only letters, numbers and hyphens."
        )

    return value


class Gender(str, Enum):
    male = "MALE"
    female = "FEMALE"
    other = "OTHER"


class VehicleType(str, Enum):
    bike = "BIKE"
    car = "CAR"
    auto = "AUTO"


class Driver(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
    )

    name: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=18)
    phone: PhoneNumber
    password: str
    email_verified: bool = False
    phone_verified: bool = Field(default=False)

    is_active: bool = True

    gender: Gender

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    rides: int = Field(default=0, ge=0)

    current_latitude: float | None = None
    current_longitude: float | None = None

    is_online: bool = False
    is_available: bool = False

    license_number: str = Field(
        unique=True,
        nullable=False,
    )

    vehicles: list["Vehicle"] = Relationship(back_populates="driver")

    @field_validator("password")
    @classmethod
    def passwordchecker(cls, value: str) -> str:
        return validate_password(value)

    @field_validator("license_number")
    @classmethod
    def license_validator(cls, value: str) -> str:
        return validate_license(value)


class User(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
    )

    name: str = Field(min_length=1)
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    age: int = Field(ge=18)
    phone: PhoneNumber
    password: str
    email_verified: bool = False

    is_active: bool = True
    gender: Gender
    phone_verified: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    @field_validator("password")
    @classmethod
    def passwordchecker(cls, value: str) -> str:
        return validate_password(value)


class Vehicle(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
    )

    vehicle_brand: str
    vehicle_name: str

    registration_number: str = Field(
        unique=True,
        nullable=False,
    )

    vehicle_type: VehicleType

    driver_id: UUID = Field(
        foreign_key="driver.id",
        nullable=False,
    )

    driver: Optional[Driver] = Relationship(back_populates="vehicles")
