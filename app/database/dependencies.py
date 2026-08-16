from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme_driver, oauth2_scheme_user
from app.database.models import Driver, User
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.driver import DriverRepository
from app.services.user import UserRepository
from app.services.vehicle import VehicleRepository
from app.utils import decode_access_token

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


# Access Token
def get_access_token_driver(token: Annotated[str, Depends(oauth2_scheme_driver)]):
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="InValid Access Token"
        )
    return data


# Logged In
async def get_current_driver(
    token_data: Annotated[dict, Depends(get_access_token_driver)], session: SessionDep
):
    try:
        driver_id = UUID(token_data["user"]["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token"
        )

    driver = await session.get(Driver, driver_id)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User No Longer exists.."
        )

    return driver


# Driver Login Dep
DriverLoginDep = Annotated[Driver, Depends(get_current_driver)]


async def get_access_token_user(token: Annotated[str, Depends(oauth2_scheme_user)]):
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Access Token"
        )
    return data


# Logged In User
async def get_current_user(
    token_data: Annotated[dict, Depends(get_access_token_user)], session: SessionDep
):
    try:
        user_id = UUID(token_data["USER"]["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token"
        )

    user = await session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User No Longer exists.."
        )
    return user


# User Login Dep
UserLoginDep = Annotated[User, Depends(get_current_user)]
