from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi import BackgroundTasks, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from app.config import app_settings
from app.core.security import oauth2_scheme_user
from app.database.redis import (
    _token_blacklist,
    add_jti_to_blacklist,
    delete_email_otp,
    delete_sms_otp,
    generate_email_otp,
    generate_phone_otp,
    generate_url_safe_token,
    is_jti_blacklisted,verify_sms_otp,

    verify_email_otp,
)
from app.schemas.user import RefreshTokenRequest
from app.security import password_hash
from app.services.notifications import NotificationService
from app.utils import (
    decode_access_token,
    decode_refresh_token,
    generate_access_token,
    generate_refresh_token,
    get_token_ttl,
)


class BaseService:
    def __init__(self, model: SQLModel, session: AsyncSession) -> None:
        self.session = session
        self.model = model
        self.notification_service = NotificationService()

    async def _get_id(self, id: UUID):
        return await self.session.get(self.model, id)

    async def _create(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)

        return entity

    async def _update(self, entity: SQLModel, update_data: dict[str, Any]):
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data to be Updated..",
            )

        entity.sqlmodel_update(update_data)

        if hasattr(entity, "updated_at"):
            entity.updated_at = datetime.now()

        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _login(self, email, password, token_key: str, role: str):
        stmt = select(self.model).where(self.model.email == email)
        res = await self.session.execute(stmt)
        user = res.scalar_one_or_none()

        if user is None or not password_hash.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="...Email or Password is incorrect..",
            )

        access_token = generate_access_token(
            data={
                token_key: {
                    "sub": str(user.id),
                    "role": role,
                }
            }
        )

        refresh_token = generate_refresh_token(
            data={
                token_key: {
                    "sub": str(user.id),
                    "role": role,
                }
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def _logout(
        self,
        token: Annotated[str, Depends(oauth2_scheme_user)],
        refresh_token: RefreshTokenRequest,
    ):
        token_data = decode_access_token(token)
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        access_ttl = get_token_ttl(token_data["exp"])
        await add_jti_to_blacklist(token_data["jti"], access_ttl)

        refresh_data = decode_refresh_token(refresh_token.refresh_token)

        if refresh_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="your_refresh_token",
            )

        refresh_ttl = get_token_ttl(refresh_data["exp"])
        await add_jti_to_blacklist(
            refresh_data["jti"],
            refresh_ttl,
        )

        return {"detail": "Logged Successfully.."}

    async def refresh(self, token_data: RefreshTokenRequest, token_key: str):
        payload = decode_refresh_token(token_data.refresh_token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        jti = payload.get("jti")

        if jti is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        if await is_jti_blacklisted(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
            )

        user_data = payload.get(token_key)

        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user_id = user_data.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        new_access_token = generate_access_token(
            data={
                token_key: {
                    "sub": user_id,
                    "role": user_data.get("role"),
                }
            }
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
        }

    async def delete(self, entity: SQLModel):
        await self.session.delete(entity)

    async def _change_password(
        self, current_data: SQLModel, old_password: str, new_password: str
    ):
        if not password_hash.verify(old_password, current_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is Incorrect",
            )

        if old_password == new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from old password..",
            )

        current_data.password = password_hash.hash(new_password)

        self.session.add(current_data)

        await self.session.commit()

        return {"message": "Password changed successfully"}

    async def _send_verification_otp(
        self, email: str, background_tasks: BackgroundTasks
    ):
        otp = await generate_email_otp(email)





        await self.notification_service.send_email_otp(
            email=email, otp=otp, background_tasks=background_tasks
        )

        print("message  :  Verification OTP sent successfully")

    async def _verify_email(self, email: EmailStr, otp: str):
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )

        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Not Found..",
            )

        if user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified..",
            )

        is_valid = await verify_email_otp(
            email=str(email),
            otp=otp,
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP..",
            )

        user.email_verified = True

        await self.session.commit()
        await self.session.refresh(user)

        await delete_email_otp(str(email))

        return {
            "message": "Email verified successfully",
        }



    async def _resend_verification_otp(
        self, email: str, background_task: BackgroundTasks
    ):
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )

        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not Found.."
            )

        if user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email is already verfied...",
            )

        otp = await generate_email_otp()

        await store_email_otp(email=email, otp=otp, ttl=600)

        await self.notification_service.send_email_otp(
            email=email, otp=otp, background_tasks=background_task
        )

        return {"message": "OTP sent successfully"}

    async def _forgot_password(
        self,
        email: EmailStr,
        router_prefix: str,
        background_tasks: BackgroundTasks,
    ):
        res = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )

        user = res.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not Found.."
            )

        token = await generate_url_safe_token(user=user)

        reset_url = (
            f"http://{app_settings.APP_DOMAIN}"
            f"{router_prefix}/reset-password?token={token}"
        )

        await self.notification_service.send_email_password_token(
            email=email, token=reset_url, background_task=background_tasks
        )

        return {"message": "Mail Sent Successfully.."}

    async def _reset_password(
        self,
        token: str,
        new_password: str,
    ):
        key = f"reset:{token}"

        user_id = await _token_blacklist.get(key)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        user_id = UUID(user_id.decode("utf-8"))

        user = await self.session.get(self.model, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.password = password_hash.hash(new_password)

        await self.session.commit()

        await _token_blacklist.delete(key)

        return {"message": "Password reset successfully"}

    async def _send_sms_otp(self, email: str, background_tasks: BackgroundTasks):
        res = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        user = res.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found.."
            )

        if user.phone_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone Number already Verified..",
            )

        otp = await generate_phone_otp(phone=user.phone, ttl=600)

        await self.notification_service.send_sms_otp(
            email=email, otp=otp, background_tasks=background_tasks
        )

        print("Message : SMS sent Succesfully..")

    async def _verify_phonenumber(self, phone: str, otp: str):
        res = await self.session.execute(
            select(self.model).where(self.model.phone == phone)
        )

        user = res.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not Found..."
            )

        if user.phone_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone Already Verifed..",
            )

        is_valid = await verify_sms_otp(phone, otp)

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or exipred otp..",
            )

        user.phone_verified = True

        await self.session.commit()
        await self.session.refresh(user)

        await delete_sms_otp(phone)

        return {"message": "Phone  verified successfully"}
