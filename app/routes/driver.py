from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.core.security import oauth2_scheme_driver
from app.database.dependencies import DriverLoginDep, DriverServiceDep, SessionDep
from app.schemas.driver import ChangePassword, DriverCreate, DriverRespone, DriverUpdate
from app.schemas.notifications import EmailVerification
from app.schemas.user import RefreshTokenRequest

router = APIRouter(prefix="/drivers", tags=["Driver"])


@router.get("/id", response_model=DriverRespone)
async def get_id_driver(id: UUID, service: DriverServiceDep):
    return await service.get_id(id)


@router.post("/register")
async def create_driver(driver_creditinals: DriverCreate, service: DriverServiceDep,background_task:BackgroundTasks):
    return await service.create_driver(driver_creditinals,background_task)


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


@router.post("/login")
async def login_driver(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DriverServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {
        "message": "...Login Successfull..",
        "access_token": token["access_token"],
        "refresh_token": token["refresh_token"],
        "token_type": "bearer",
    }


@router.get("/me", response_model=DriverRespone)
async def get_me(current_user: DriverLoginDep):
    return current_user


@router.patch("/change_password")
async def change_password(
    password_data: ChangePassword,
    current_data: DriverLoginDep,
    service: DriverServiceDep,
):
    return await service.change_password(current_data, password_data)


@router.post("/refresh")
async def refresh_token(
    token_data: RefreshTokenRequest, session: SessionDep, service: DriverServiceDep
):

    return await service.refresh_access_token(token_data.refresh_token)


@router.post("/logout")
async def logout_driver(
    token: Annotated[str, Depends(oauth2_scheme_driver)],
    refresh_token: RefreshTokenRequest,
    session: SessionDep,
    service: DriverServiceDep,
):

    return await service.logout_driver(
        token,
        refresh_token.refresh_token,
    )


@router.post("/verify-email")
async def verify_email(vefiy: EmailVerification, service: DriverServiceDep):
    return await service.verify_email(email=vefiy.email, otp=vefiy.otp)


@router.post("/resend-verfication")
async def resend_otp(
    email: EmailStr, background_task: BackgroundTasks, service: DriverServiceDep
):
    return await service.resend_verification_otp(email, background_task)
