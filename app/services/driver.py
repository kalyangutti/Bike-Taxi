from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Driver
from app.schemas.driver import (
    ChangePassword,
    DriverCreate,
    DriverUpdate,
)
from app.security import password_hash
from app.services.base import BaseService


class DriverRepository(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Driver, session)

    async def get_id(self, id: UUID):
        return await self._get_id(id)

    async def create_driver(
        self, driver_create: DriverCreate, background_task: BackgroundTasks
    ):

        driver = Driver(
            **driver_create.model_dump(
                exclude={"password", "created_at", "updated_at"}
            ),
            password=password_hash.hash(driver_create.password),
        )

        driver = await self._create(driver)

        await self._send_verification_otp(driver.email, background_task)
        return {
            "message": "Created Successfully. Verification OTP sent to your email.",
            "new_id": driver.id,
        }

    async def update_driver(
        self,
        driver: Driver,
        driver_update: DriverUpdate,
    ):
        update_data = driver_update.model_dump(exclude_none=True)

        return await self._update(driver, update_data)

    async def delete_driver(self, driver: Driver):
        await self.session.delete(driver)
        await self.session.commit()

        return {"message": f"Driver {driver.id} deleted successfully."}

    async def change_password(
        self,
        current_data: Driver,
        password_data: ChangePassword,
    ):
        return await self._change_password(
            current_data,
            password_data.old_password,
            password_data.new_password,
        )

    async def login(self, email: str, password: str):
        return await self._login(
            email=email,
            password=password,
            token_key="DRIVER",
            role="driver",
        )

    async def logout_driver(
        self,
        access_token: str,
        refresh_token: str,
    ):
        return await self._logout(
            access_token,
            refresh_token,
        )

    async def refresh_access_token(self, refresh_token: str):
        from app.schemas.user import RefreshTokenRequest

        token_data = RefreshTokenRequest(refresh_token=refresh_token)

        return await self.refresh(
            token_data,
            token_key="DRIVER",
        )

    async def verify_email(self, email: str, otp: int):
        return await self._verify_email(email, otp)

    async def resend_verification_otp(
        self, email: str, background_task: BackgroundTasks
    ):
        return await super()._resend_verification_otp(email, background_task)
