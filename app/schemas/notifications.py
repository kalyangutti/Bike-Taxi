from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import PhoneNumber


class EmailVerification(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)

class PhoneVerification(BaseModel):
    phone:PhoneNumber
    otp: str = Field(min_length=6, max_length=6)
