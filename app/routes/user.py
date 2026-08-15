from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database.dependencies import UserLoginDep, UserServiceDep
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
current_user:UserLoginDep,user_update: UserDetailsUpdate, service: UserServiceDep
):
    return await service.update_user(current_user, user_update)


@router.delete("/me")
async def delete_user(current_user:UserLoginDep, service: UserServiceDep):
    return await service.delete_user_by_id(current_user)


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


@router.post("/login")
async def login_user(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token["token"], "token_type": "bearer"}


@router.get("/me", response_model=UserRespone)
async def get_me(current_user: UserLoginDep):
    return current_user
