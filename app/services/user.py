from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.schemas.user import (
    ChangePassword,
    RefreshTokenRequest,
    UserCreate,
    UserDetailsUpdate,
)
from app.security import password_hash
from app.services.base import BaseService


class UserRepository(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        self.model = User
        super().__init__(self.model, session)

    async def get_id(self, id: UUID):
        return await self._get_id(id)

    async def create_user(
        self,
        user_data: UserCreate,
        background_tasks: BackgroundTasks,
    ):
        user = User(
            **user_data.model_dump(exclude={"password", "created_at", "updated_at"}),
            password=password_hash.hash(user_data.password),
        )

        user = await self._create(user)

        await self._send_verification_otp(
            user.email,
            background_tasks,
        )

        return {
            "message": "Created Successfully. Verification OTP sent to your email.",
            "new_id": user.id,
        }

    async def update_user(self, user: User, user_update: UserDetailsUpdate):
        update_data = user_update.model_dump(exclude_none=True)
        return await self._update(user, update_data)

    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
        return {"detail": f"{user.id} has been deleted from the database.."}

    async def login(self, email, password):
        return await self._login(
            email=email, password=password, token_key="USER", role="user"
        )

    async def logout(
        self,
        token: str,
        refresh_token: RefreshTokenRequest,
    ):
        return await self._logout(token, refresh_token)

    async def refresh(self, token_data: RefreshTokenRequest):
        return await super().refresh(token_data, token_key="USER")

    async def change_password(self, current_data: User, password_data: ChangePassword):
        return await self._change_password(
            current_data,
            password_data.old_password,
            password_data.new_password,
        )

    async def verify_email(self, email: str, otp: int):
        return await self._verify_email(email, otp)

    async def resend_verification_otp(self, email: str, background_task: BackgroundTasks):
        return await super()._resend_verification_otp(email, background_task)
