from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import func, select

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

    # INNER JOIN
    async def inner_join(self):
        stmt = select(Driver, Vehicle).join(Driver, Driver.id == Vehicle.driver_id)
        res = await self.session.execute(stmt)
        return res.mappings().all()

    # Left join
    async def left_join(self):
        stmt = select(Driver, Vehicle).join(
            Vehicle, Driver.id == Vehicle.driver_id, isouter=True
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    # Right Join
    async def right_join(self):
        stmt = select(Vehicle, Driver).join(
            Driver, Driver.id == Vehicle.driver_id, isouter=True
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    # Full Join
    async def full_join(self):
        stmt = select(Vehicle, Driver).join(
            Driver, Driver.id == Vehicle.driver_id, full=True
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    # Cross Join
    async def cross_join(self):
        stmt = select(Driver, Vehicle)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    # How Many Number of Vehicles
    async def count(self):
        stmt = (
            select(Driver.name, func.count(Vehicle.id).label("Vehicle Count"))
            .join(Vehicle, Driver.id == Vehicle.driver_id)
            .group_by(Driver.id)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()
