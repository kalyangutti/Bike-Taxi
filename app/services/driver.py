from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import asc, desc, select

from app.database.models import Driver
from app.schemas.driver import DriverCreate, DriverUpdate
from app.security import password_hash
from app.utils import generate_access_token


class DriverRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_id(self, id: UUID):
        driver = await self.session.get(Driver, id)

        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Driver with id {id} not found.",
            )

        return driver

    async def create_driver(self, driver_create: DriverCreate):
        driver = Driver(
            **driver_create.model_dump(
                exclude={"password", "created_at", "updated_at"}
            ),
            password=password_hash.hash(driver_create.password),
        )

        self.session.add(driver)
        await self.session.commit()
        await self.session.refresh(driver)

        return driver

    async def update_driver(self, driver: Driver, driver_update: DriverUpdate):

        update_data = driver_update.model_dump(exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided.",
            )

        driver.sqlmodel_update(update_data)
        driver.updated_at = datetime.now()

        self.session.add(driver)
        await self.session.commit()
        await self.session.refresh(driver)

        return driver

    async def delete_driver(self, driver: Driver):

        await self.session.delete(driver)
        await self.session.commit()

        return {"message": f"Driver {driver.id} deleted successfully."}

    async def sorting(self, sort_by: str = "name", order: str = "asc"):
        column = getattr(Driver, sort_by, None)

        if column is None:
            raise ValueError("Invalid Sorting Field")

        stmt = select(Driver)
        if order.lower() == "desc":
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))

        result = await self.session.scalars(stmt)

        return result.all()

    async def pagination(
        self, page: int = 1, size=4, sort_by: str = "name", order: str = "asc"
    ):
        column = getattr(Driver, sort_by, "None")

        if column is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Sorting Field"
            )

        offset = (page - 1) * size

        stmt = select(Driver)

        if order.lower() == "desc":
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))

        stmt = stmt.offset(offset).limit(size)

        result = await self.session.scalars(stmt)
        return result.all()

    async def token(self, email, password) -> str:
        stmt = select(Driver).where(Driver.email == email)
        result = await self.session.execute(stmt)
        driver = result.scalar_one_or_none()

        if driver is None or not password_hash.verify(password, driver.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="..Email or Password is incorrect..",
            )

        token = generate_access_token(
            data={"user": {"sub": str(driver.id), "role": "driver"}}
        )
        return token
