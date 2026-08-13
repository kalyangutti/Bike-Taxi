from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.database.dependencies import VehicleServiceDep
from app.schemas.respones import (
    CrossJoinResponse,
    DriverVehicleRespone,
    VehicleDriverRespone,
    VehicleResponeDriverRespone,
)
from app.schemas.vehicles import VehicleCreate

router = APIRouter(prefix="/vehicle", tags=["Vehicle"])


@router.get("/id")
async def get_id_vehicle(id: UUID, service: VehicleServiceDep):
    return await service.get_id(id)


@router.post("/register")
async def create_vehicle(vehicle_create: VehicleCreate, service: VehicleServiceDep):
    return await service.create_vehicle(vehicle_create)


@router.delete("/id")
async def delete(id: UUID, service: VehicleServiceDep):
    return await service.delete(id)


@router.get("/inner_join")
async def inner_join(service: VehicleServiceDep):
    return await service.inner_join()


@router.get("/left_join", response_model=List[DriverVehicleRespone])
async def left_join(service: VehicleServiceDep):
    return await service.left_join()


@router.get("/right_join", response_model=List[VehicleDriverRespone])
async def right_join(service: VehicleServiceDep):
    return await service.right_join()


@router.get("/full_join", response_model=List[VehicleResponeDriverRespone])
async def full_join(service: VehicleServiceDep):
    return await service.full_join()


@router.get("/cross_join")
async def cross_join(
    service: VehicleServiceDep, response_model=List[CrossJoinResponse]
):
    return await service.cross_join()


@router.get("/count")
async def count(service: VehicleServiceDep):
    return await service.count()
