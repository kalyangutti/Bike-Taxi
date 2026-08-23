from pydantic import BaseModel, EmailStr, Field


class EmailVerification(BaseModel):
    email: EmailStr
    otp: int = Field(ge=100000, le=999999)
