from passlib.context import CryptContext

password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")
