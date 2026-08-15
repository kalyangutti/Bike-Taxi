from fastapi.security import OAuth2PasswordBearer

oauth2_scheme_driver = OAuth2PasswordBearer(tokenUrl="/drivers/token")

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/user/login")
