from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import asc, desc, select

from app.database.models import Driver
from app.schemas.driver import DriverCreate, DriverUpdate
from app.security import password_hash


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

    async def update_driver(self, id: UUID, driver_update: DriverUpdate):
        driver = await self.get_id(id)

        update_data = driver_update.model_dump(exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided.",
            )

        driver.sqlmodel_update(update_data)

        self.session.add(driver)
        await self.session.commit()
        await self.session.refresh(driver)

        return driver

    async def delete_driver(self, id: UUID):
        driver = await self.get_id(id)

        await self.session.delete(driver)
        await self.session.commit()

        return {"message": f"Driver {id} deleted successfully."}

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

    async def get_all_users(self):
        stmt = select(Driver)

        result = await self.session.scalars(stmt).all()
        return result
