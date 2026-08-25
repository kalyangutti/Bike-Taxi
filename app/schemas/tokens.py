

from pydantic import BaseModel, Field, field_validator
from app.schemas.user import validate_password


class ResetPassword(BaseModel):
    token:str
    new_password:str = Field(min_length =6)
    @field_validator('new_password')
    @classmethod
    def validate(cls, value)->str:
        return validate_password(value)
