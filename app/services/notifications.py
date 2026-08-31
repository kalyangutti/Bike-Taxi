from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from twilio.rest import Client

from app.config import email_notifications_settings, sms_settings


class NotificationService:
    def __init__(self):
        conn = ConnectionConfig(**email_notifications_settings.model_dump())
        self.fastmail = FastMail(conn)
        self.twilio_client = Client(
            sms_settings.TWILO_SID,
            sms_settings.TWILO_AUTH_TOKEN,
        )

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

    async def send_email_password_token(
        self,
        email: EmailStr,
        token: str,
        background_task: BackgroundTasks,
    ):
        subject = "Bike Taxi - Password Reset"

        body = f"""
    Reset your password using the link below:

    {token}

    This link will expire in 15 minutes.
    """

        await self.send_email(
            recipients=[email],
            subject=subject,
            body=body,
            background_tasks=background_task,
        )

    async def _send_sms(
        self,
        recipients: EmailStr,
        subject: str,
        body: str,
        background_tasks: BackgroundTasks,
    ):
        messgae = MessageSchema(
            recipients=recipients, subject=subject, body=body, subtype=MessageType.plain
        )
        print("ADDING SMS BACKGROUND TASK")

        background_tasks.add_task(self.fastmail.send_message, message=messgae)

        print("SMS SENT SUCCESSFULLY....!")

    async def send_sms_otp(
        self,
        email: str,
        otp: str,background_tasks: BackgroundTasks):
        body = f"""
    Your Bike Taxi verification OTP is:

    {otp}

    This OTP is valid for 10 minutes.

    If you did not request this verification, please ignore this message.
    """

        await self._send_sms(
            recipients=[email],
            subject="Bike Taxi SMS System..",
            body=body,
            background_tasks=background_tasks,
        )
