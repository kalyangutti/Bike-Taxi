from uuid import UUID

from pydantic import BaseModel

from app.database.models import VehicleType


class VehicleBase(BaseModel):
    vehicle_brand: str
    vehicle_name: str
    registration_number: str
    vehicle_type: VehicleType


class VehicleCreate(VehicleBase):
    driver_id: UUID


class VehicleRead(VehicleBase):
    id: UUID
    driver_id: UUID
