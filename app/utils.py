from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from app.config import security_settings


def generate_access_token(data: dict, exipry: timedelta = timedelta(days=7)) -> str:
    token = jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + exipry,
            "type": "access",
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )
    return token


def decode_access_token(token: str):
    print("TOKEN:", repr(token))
    print("DOT COUNT:", token.count("."))
    print("PARTS:", len(token.split(".")))

    try:
        payload = jwt.decode(
            token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )

        print("PAYLOAD:", payload)

        if payload.get("type") != "access":
            print("Not an access token..")
            return None
        return payload

    except Exception as e:
        print("JWT ERROR:", repr(e))
        return None


def generate_refresh_token(data: dict, exipry: timedelta = timedelta(days=7)):
    token = jwt.encode(
        payload={**data,"jti": str(uuid4()),"exp": datetime.now(timezone.utc) + exipry, "type": "refresh"},
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )
    return token


def decode_refresh_token(token: str):
    print("TOKEN:", repr(token))
    print("DOT COUNT:", token.count("."))
    print("PARTS:", len(token.split(".")))

    try:
        payload = jwt.decode(
            token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )

        print("PAYLOAD:", payload)

        if payload.get("type") != "refresh":
            print("Not an refresh token..")
            return None
        return payload

    except Exception as e:
        print("JWT ERROR:", repr(e))
        return None


def get_token_ttl(exp: int) -> int:
    remaining = exp - int(datetime.now(timezone.utc).timestamp())

    return max(remaining, 1)
