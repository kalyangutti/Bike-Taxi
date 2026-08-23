from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config import notifications_settings


class NotificationService:
    def __init__(self):
        conn = ConnectionConfig(**notifications_settings.model_dump())
        self.fastmail = FastMail(conn)

    async def send_email(
    self,
    recipients: list[EmailStr],
    subject: str,
    body: str,
    background_tasks: BackgroundTasks,
):
        message = MessageSchema(
            recipients=recipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain,
        )

        print("ADDING EMAIL BACKGROUND TASK")

        background_tasks.add_task(
            self.fastmail.send_message,
            message=message,
        )

    async def send_email_otp(
        self,
        email: EmailStr,
        otp: str,
        background_tasks: BackgroundTasks,
    ):
        subject = "Bike Taxi - Email Verification"

        body = f"""
Hello,

Your Bike Taxi email verification OTP is:

{otp}

This OTP is valid for 10 minutes.

If you did not request this verification, please ignore this email.

Regards,
Bike Taxi Team
"""

        await self.send_email(
            recipients=[email],
            subject=subject,
            body=body,
            background_tasks=background_tasks,
        )
