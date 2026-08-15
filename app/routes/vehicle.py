from uuid import UUID

from fastapi import APIRouter

from app.database.dependencies import VehicleServiceDep
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
