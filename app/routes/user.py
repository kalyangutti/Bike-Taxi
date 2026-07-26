from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.database.dependencies import UserServiceDep
from app.schemas.user import UserCreate, UserDetailsUpdate, UserRead, UserRespone

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/id", response_model=UserRead)
async def get_id(id: UUID, service: UserServiceDep):
    user = await service.get_id(id)
    return user


@router.post("/register")
async def create_user(user: UserCreate, service: UserServiceDep):
    return await service.create_user(user)


@router.patch("/update", response_model=UserRead)
async def update_user(
    id: UUID, user_update: UserDetailsUpdate, service: UserServiceDep
):
    return await service.update_user(id, user_update)


@router.delete("/id")
async def delete_user(id: UUID, service: UserServiceDep):
    return await service.delete_user_by_id(id)


@router.get("/all/ids", response_model=List[UserRespone])
async def get_all_users(service: UserServiceDep):
    return await service.get_all_user()


@router.get("/sort", response_model=List[UserRespone])
async def get_users(service: UserServiceDep, sort_by: str = "name", order: str = "asc"):
    return await service.sort_users(sort_by, order)


@router.get("/sort&pagination", response_model=List[UserRespone])
async def sorting_pagination(
    page: int,
    size: int,
    service: UserServiceDep,
    sort_by: str = "name",
    order: str = "asc",
):
    return await service.pagination(page, size, sort_by, order)
