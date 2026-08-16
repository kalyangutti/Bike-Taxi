from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import oauth2_scheme_user
from app.database.dependencies import UserLoginDep, UserServiceDep
from app.database.redis import add_jti_to_blacklist, is_jti_blacklisted
from app.schemas.user import (
    RefreshTokenRequest,
    UserCreate,
    UserDetailsUpdate,
    UserRead,
    UserRespone,
)
from app.utils import (
    decode_access_token,
    decode_refresh_token,
    generate_access_token,
    get_token_ttl,
)

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/id", response_model=UserRead)
async def get_id(id: UUID, service: UserServiceDep):
    user = await service.get_id(id)
    return user


@router.post("/register")
async def create_user(user: UserCreate, service: UserServiceDep):
    return await service.create_user(user)


@router.patch("/update", response_model=UserRead)
async def update_user(
    current_user: UserLoginDep, user_update: UserDetailsUpdate, service: UserServiceDep
):
    return await service.update_user(current_user, user_update)


@router.delete("/me")
async def delete_user(current_user: UserLoginDep, service: UserServiceDep):
    return await service.delete_user_by_id(current_user)


@router.get("/all/ids", response_model=List[UserRespone])
async def get_all_users(service: UserServiceDep):
    return await service.get_all_user()


@router.get("/sort", response_model=List[UserRespone])
async def get_users(service: UserServiceDep, sort_by: str = "name", order: str = "asc"):
    return await service.sort_users(sort_by, order)


@router.get("/sort&pagination", response_model=List[UserRespone])
async def sorting_pagination(
    page: int,
    size: int,
    service: UserServiceDep,
    sort_by: str = "name",
    order: str = "asc",
):
    return await service.pagination(page, size, sort_by, order)


@router.post("/login")
async def login_user(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token["access_token"],
        "refresh_token": token["refresh_token"],
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserRespone)
async def get_me(current_user: UserLoginDep):
    return current_user


# Refresh Token
@router.post("/refresh")
async def refresh_token(token_data: RefreshTokenRequest):
    payload = decode_refresh_token(token_data.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired referesh token..",
        )

    jti = payload.get("jti")

    if jti is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Refresh Token"
        )

    if await is_jti_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
        )

    user_data = payload.get("USER")

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    user_id = user_data.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    new_access_token = generate_access_token(
        data={"USER": {"sub": user_id, "role": user_data.get("role")}}
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_user(
    token: Annotated[str, Depends(oauth2_scheme_user)],
    refresh_token: RefreshTokenRequest,
):
    token_data = decode_access_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
    access_ttl = get_token_ttl(token_data["exp"])

    await add_jti_to_blacklist(token_data["jti"], access_ttl)

    refresh_data = decode_refresh_token(refresh_token.refresh_token)

    if refresh_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="your_refresh_token"
        )

    refresh_ttl = get_token_ttl(refresh_data["exp"])

    await add_jti_to_blacklist(
        refresh_data["jti"],
        refresh_ttl,
    )

    return {"detail": "Logged Successfully.."}
