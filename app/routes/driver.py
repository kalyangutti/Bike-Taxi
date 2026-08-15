from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database.dependencies import DriverLoginDep, DriverServiceDep
from app.schemas.driver import DriverCreate, DriverRespone, DriverUpdate

router = APIRouter(prefix="/drivers", tags=["Driver"])


@router.get("/id", response_model=DriverRespone)
async def get_id_driver(id: UUID, service: DriverServiceDep):
    return await service.get_id(id)


@router.post("/register", response_model=DriverRespone)
async def create_driver(driver_creditinals: DriverCreate, service: DriverServiceDep):
    return await service.create_driver(driver_creditinals)


@router.patch("/update_driver", response_model=DriverRespone)
async def upadte_driver_details(
    driver: DriverLoginDep, driver_details: DriverUpdate, service: DriverServiceDep
):
    return await service.update_driver(driver, driver_details)


@router.delete("/id")
async def delete_driver_by_uuid(driver: DriverLoginDep, service: DriverServiceDep):
    return await service.delete_driver(driver)


@router.get("/sorting", response_model=List[DriverRespone])
async def custom_flitering(
    service: DriverServiceDep, sort_by: str = "name", order: str = "asc"
):
    return await service.sorting(sort_by, order)


@router.get("/pagination", response_model=DriverRespone)
async def pagination(
    service: DriverServiceDep,
    page: int = 1,
    size: int = 4,
    sort_by: str = "name",
    order: str = "asc",
):
    return await service.pagination(page, size, sort_by, order)


@router.post("/token")
async def login_driver(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DriverServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=DriverRespone)
async def get_me(current_user: DriverLoginDep):
    return current_user
