from pydantic import BaseModel

from app.database.models import VehicleType
from app.schemas.driver import DriverRespone
from app.schemas.vehicles import VehicleRespone


class DriverVehicleRespone(BaseModel):
    Driver: DriverRespone
    Vehicle: VehicleRespone | None


class VehicleDriverRespone(BaseModel):
    Driver: DriverRespone | None
    Vehicle: VehicleRespone


class VehicleResponeDriverRespone(BaseModel):
    Driver: DriverRespone | None
    Vehicle: VehicleRespone | None


from uuid import UUID

from pydantic import BaseModel


class CrossJoinResponse(BaseModel):
    driver_id: UUID
    driver_name: str
    driver_age: int

    vehicle_id: UUID
    vehicle_name: str
    vehicle_brand: str
    vehicle_type: VehicleType
    registration_number: str
