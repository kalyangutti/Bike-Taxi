from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.database.dependencies import DriverServiceDep
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
    id: UUID, driver_details: DriverUpdate, service: DriverServiceDep
):
    return await service.update_driver(id, driver_details)


@router.delete("/id")
async def delete_driver_by_uuid(id: UUID, service: DriverServiceDep):
    return await service.delete_driver(id)


@router.get("/sorting", response_model=List[DriverRespone])
async def custom_flitering(
    service: DriverServiceDep, sort_by: str = "name", order: str = "asc"
):
    return await service.sorting(sort_by, order)


@router.get("/pagination", response_model=List[DriverRespone])
async def pagination(
    service: DriverServiceDep,
    page: int = 1,
    size: int = 4,
    sort_by: str = "name",
    order: str = "asc",
):
    return await service.pagination(page, size, sort_by, order)


@router.get("/allsuer", response_model=List[DriverRespone])
async def get_all_user(service: DriverServiceDep):
    return await service.get_all_users()
