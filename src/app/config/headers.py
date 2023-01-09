from fastapi import Header, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from config.variables import API_KEY, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from services import user_service

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = {"user_id": user_id}
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_by_id(
        id=token_data.get("user_id"))
    if not user:
        raise credentials_exception
    return user


async def get_api_key_header(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API Key is not valid")
