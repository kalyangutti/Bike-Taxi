from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.database.models import Driver, Vehicle
from app.schemas.vehicles import VehicleCreate


class VehicleRepository:
    def __init__(self, session):
        self.session = session

    async def get_id(self, id: UUID):
        vehicle = await self.session.get(Vehicle, id)

        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not Found in the database..",
            )
        return vehicle

    async def create_vehicle(self, vehicle_create: VehicleCreate):
        vehicle_details = Vehicle(**vehicle_create.model_dump())
        self.session.add(vehicle_details)
        await self.session.commit()
        await self.session.refresh(vehicle_details)
        return vehicle_details

    async def delete(self, id: UUID):
        vehicle_details = await self.get_id(id)
        await self.session.delete(vehicle_details)
        await self.session.commit()
        return {"detail": f"Id {id} is deleted from the database..."}

    