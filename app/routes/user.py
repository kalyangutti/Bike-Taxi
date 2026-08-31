from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.core.security import oauth2_scheme_user
from app.database.dependencies import UserLoginDep, UserServiceDep
from app.schemas.notifications import EmailVerification, PhoneVerification
from app.schemas.user import (
    ChangePassword,
    RefreshTokenRequest,
    UserCreate,
    UserDetailsUpdate,
    UserRead,
    UserRespone,
)
from app.schemas.tokens import ResetPassword
from app.utils import (
    decode_refresh_token,
)

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/id", response_model=UserRead)
async def get_id(id: UUID, service: UserServiceDep):
    user = await service.get_id(id)
    return user


@router.post("/register")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    service: UserServiceDep,
):
    return await service.create_user(user, background_tasks)


@router.patch("/update", response_model=UserRead)
async def update_user(
    current_user: UserLoginDep, user_update: UserDetailsUpdate, service: UserServiceDep
):
    return await service.update_user(current_user, user_update)


@router.delete("/me")
async def delete_user(current_user: UserLoginDep, service: UserServiceDep):
    return await service.delete_user_by_id(current_user)


@router.post("/login")
async def login_user(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {
        "access_token": token["access_token"],
        "refresh_token": token["refresh_token"],
        "token_type": "bearer",
    }


@router.put("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user: UserLoginDep,
    service: UserServiceDep,
):
    return await service.change_password(current_user, password_data)


@router.get("/me", response_model=UserRespone)
async def get_me(current_user: UserLoginDep):
    return current_user


@router.post("/refresh")
async def refresh_token(token_data: RefreshTokenRequest, service: UserServiceDep):
    payload = decode_refresh_token(token_data.refresh_token)
    return payload


@router.post("/logout")
async def logout_user(
    token: Annotated[str, Depends(oauth2_scheme_user)],
    refresh_token: RefreshTokenRequest,
    service: UserServiceDep,
):
    return service.logout(token, refresh_token)


@router.post("/verify-email")
async def verify_email(
    verify: EmailVerification,
    service: UserServiceDep,
):
    return await service.verify_email(
        email=verify.email,
        otp=verify.otp,
    )


@router.post("/resend-verfication")
async def resend_verfication(
    email: EmailStr, background_tasks: BackgroundTasks, service: UserServiceDep
):
    return await service.resend_verification_otp(email, background_tasks)

@router.post('/forgot-password')
async def forgot_password(email:EmailStr,background_task:BackgroundTasks,service:UserServiceDep):
    return await service.forgot_password(email,router.prefix,background_task)


@router.post('/reset-password')
async def reset_password(password_data:ResetPassword,service:UserServiceDep):
    return await service.reset_password(password_data)


@router.post('/verify-phonenumber')
async def verify_phonenumber(verify:PhoneVerification,service:UserServiceDep):
    return await service.verify_phonenumber(verify.phone,verify.otp)
