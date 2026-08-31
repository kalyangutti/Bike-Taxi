import secrets

from redis.asyncio import Redis

from app.config import db_settings
from app.security import password_hash


_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=0,
)

_message_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=1,
)


async def add_jti_to_blacklist(jti: str, ttl: int):
    await _token_blacklist.set(
        jti,
        "blacklisted",
        ex=ttl,
    )


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti)


# =========================
# EMAIL OTP
# =========================


async def generate_email_otp(email: str) -> str:
    otp = f"{secrets.randbelow(1_000_000):06d}"

    otp_hash = password_hash.hash(otp)

    key = f"email:{email}"

    await _message_blacklist.set(
        key,
        otp_hash,
        ex=600,
    )

    return otp


async def verify_email_otp(email: str, otp: str) -> bool:
    key = f"email:{email}"

    otp_hash = await _message_blacklist.get(key)

    if not otp_hash:
        return False

    if isinstance(otp_hash, bytes):
        otp_hash = otp_hash.decode()

    return password_hash.verify(otp, otp_hash)


async def delete_email_otp(email: str):
    key = f"email:{email}"

    await _message_blacklist.delete(key)


# =========================
# PASSWORD RESET TOKEN
# =========================


async def generate_url_safe_token(user):
    token = secrets.token_urlsafe(32)

    key = f"reset:{token}"

    await _token_blacklist.set(
        key,
        str(user.id),
        ex=900,
    )

    return token


# =========================
# PHONE OTP
# =========================


async def generate_phone_otp(phone: str, ttl: int):
    otp = "".join(secrets.choice("0123456789") for _ in range(6))

    sms_hashed_otp = password_hash.hash(otp)

    key = f"PhoneNumber:{phone}"

    await _message_blacklist.set(
        key,
        sms_hashed_otp,
        ex=ttl,
    )

    return otp


async def verify_sms_otp(phone: str, otp: str) -> bool:
    key = f"PhoneNumber:{phone}"

    sms_hash_otp = await _message_blacklist.get(key)

    if not sms_hash_otp:
        return False

    if isinstance(sms_hash_otp, bytes):
        sms_hash_otp = sms_hash_otp.decode()

    return password_hash.verify(
        otp,
        sms_hash_otp,
    )


async def delete_sms_otp(phone: str):
    key = f"PhoneNumber:{phone}"

    await _message_blacklist.delete(key)
