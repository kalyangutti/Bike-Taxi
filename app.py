from twilio.rest import Client
from app.config import sms_settings

account_sid = sms_settings.TWILO_SID
auth_token = sms_settings.TWILO_AUTH_TOKEN

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_=sms_settings.TWILO_NUMBER,  # Your Twilio number
    to=9014929583,  # Your verified phone number
    body="Hello from Bike Taxi! Your OTP is 123456",
)

print("SMS sent!")
print("Message SID:", message.sid)
