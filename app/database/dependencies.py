from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.services.driver import DriverRepository
from app.services.user import UserRepository
from app.services.vehicle import VehicleRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: SessionDep):
    return UserRepository(session)


UserServiceDep = Annotated[SessionDep, Depends(get_user_service)]


def get_driver_service(session: SessionDep):
    return DriverRepository(session)


DriverServiceDep = Annotated[SessionDep, Depends(get_driver_service)]


def get_vehicle_service(session: SessionDep):
    return VehicleRepository(session)


VehicleServiceDep = Annotated[SessionDep, Depends(get_vehicle_service)]
