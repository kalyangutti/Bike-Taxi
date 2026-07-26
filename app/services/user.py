from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.models import User
from app.schemas.user import UserCreate, UserDetailsUpdate
from app.security import password_hash


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_id(self, id: UUID):
        user = await self.session.get(User, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{id} is not presnet in database...",
            )
        return user

    async def create_user(self, user_data: UserCreate):
        user = User(
            **user_data.model_dump(exclude={"password", "created_at", "updated_at"}),
            password=password_hash.hash(user_data.password),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return {"Messgae": "Updated Successfully", "new_id": user.id}

    async def update_user(self, id: UUID, user_update: UserDetailsUpdate):

        user = await self.session.get(User, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found"
            )

        update = user_update.model_dump(exclude_none=True)
        if not update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided",
            )

        user.sqlmodel_update(update)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user_by_id(self, id: UUID):
        user = await self.get_id(id)
        await self.session.delete(user)
        await self.session.commit()
        return {"detail": f"{id} has been deleted from the database.."}

    async def get_all_user(self):
        stmt = select(User)

        result = await self.session.scalars(stmt)
        users = result.all()

        return users

    async def sort_users(self, sort_by="name", order: str = "asc"):
        column = getattr(User, sort_by, None)

        if column is None:
            raise ValueError("InValid Sorting Field")

        stmt = select(User)

        if order.lower() == "desc":
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))

        result = await self.session.scalars(stmt)

        return result.all()

    async def pagination(
        self,
        page: int = 1,
        size: int = 4,
        sort_by: str = "name",
        order: str = "asc",
    ):
        column = getattr(User, sort_by, None)

        if column is None:
            raise HTTPException(status_code=400, detail="Invalid sorting field")

        offset = (page - 1) * size

        stmt = select(User)

        if order.lower() == "desc":
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))

        stmt = stmt.offset(offset).limit(size)

        result = await self.session.execute(stmt)

        users = result.scalars().all()

        return users
