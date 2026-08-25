import secrets

from redis.asyncio import Redis

from app.config import db_settings
from app.security import password_hash

_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=0,
)


async def add_jti_to_blacklist(jti: str, ttl: int):
    await _token_blacklist.set(
        jti,
        "blacklisted",
        ex=ttl,
    )


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti)


async def generate_email_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


async def store_email_otp(email: str, otp: str, ttl: int = 600):
    otp_hash = password_hash.hash(otp)

    key = f"email:{email}"

    await _token_blacklist.set(key, otp_hash, ex=ttl)


async def verify_email_otp(email: str, otp: str) -> bool:
    key = f"email:{email}"

    otp_hash = await _token_blacklist.get(key)

    if not otp_hash:
        return False

    return password_hash.verify(otp, otp_hash)


async def delete_email_otp(email: str):
    key = f"email:{email}"
    await _token_blacklist.delete(key)


async def generate_url_safe_token(user):
    token = secrets.token_urlsafe(32)
    key = f"reset:{token}"

    await _token_blacklist.set(key, str(user.id), ex=900)

    return token
