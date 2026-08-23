import asyncio

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import notifications_settings

conn = ConnectionConfig(**notifications_settings.model_dump())

fastmail = FastMail(conn)


async def send_message():
    await fastmail.send_message(
        message=MessageSchema(
            recipients=["kalyangutti19@gmail.com"],
            subject="Your Email Delivered With FastShip..",
            body="...Things are about to get Interesting..",
            subtype=MessageType.plain,
        )
    )
    print("Email Sent..")


asyncio.run(send_message())
