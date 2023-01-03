from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from utils import security
from services import user_service
from config.variables import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models.token import Token
from models.login import Login
from models.user import User
from config.headers import get_current_user

router = APIRouter()


def authenticate_user(username: str, password: str) -> User | None:
    user = user_service.get_user_by_username(username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_autentication(login: Login) -> Token:
    result_login = authenticate_user(login.username, login.password)
    if not result_login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(result_login.id)}, expires_delta=access_token_expires)
    token = Token(
        access_token=access_token,
        token_type="bearer"
    )
    return token


@router.post("/login", response_model=Token)
async def get_login(login: Login):
    return get_autentication(login=login)


@router.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return get_autentication(Login(username=form_data.username, password=form_data.password))


@router.get("/users/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    user = User(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name
    )
    return user
