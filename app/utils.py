from datetime import datetime, timedelta, timezone

import jwt

from app.config import security_settings


def generate_access_token(
    data: dict, exipry: timedelta = timedelta(days=12)
) -> str:
    token = jwt.encode(
        payload={
            **data,
            "exp": datetime.now(timezone.utc) + exipry,
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
        return payload

    except Exception as e:
        print("JWT ERROR:", repr(e))
        return None
