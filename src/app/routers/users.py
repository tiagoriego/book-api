from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from utils import security
from services import user_service
from config.variables import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models.token import Token
from models.login import Login
from models.user import User, UpdateUser, UpdatePassowrd, InsertUser
from schemas.user import User as UserSchema
from config.headers import get_current_user, get_api_key_header
from utils.field import is_valid_email

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


@router.post("/login", response_model=Token, tags=["login"])
async def get_login(login: Login):
    return get_autentication(login=login)


@router.post("/token", response_model=Token, tags=["login"])
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return get_autentication(Login(username=form_data.username, password=form_data.password))


@router.get("/users/me", response_model=User, tags=["users"])
async def get_me(current_user: User = Depends(get_current_user)):
    user = User(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name
    )
    return user


@router.patch("/users", response_model=User, tags=["users"])
async def update_user(user: UpdateUser, current_user: User = Depends(get_current_user)):
    user_email = user_service.get_user_by_email(email=user.email)
    if user_email:
        if user_email.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email cannot be used.")

    if not is_valid_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not valid.")

    result = user_service.update_partial_user(
        id=current_user.id,
        full_name=user.full_name,
        email=user.email)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to update user.")

    same_user = user_service.get_user_by_id(current_user.id)
    return User(id=same_user.id,
                full_name=same_user.full_name,
                username=same_user.username,
                email=same_user.email)


@router.patch("/users/password", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def update_user_password(user: UpdatePassowrd, current_user: User = Depends(get_current_user)):

    if user.old_password == user.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Old password it is the same new password.")

    old_user_password = user_service.get_user_by_id(current_user.id)
    if not old_user_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if not security.verify_password(user.old_password, old_user_password.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Old password does not match.")

    result = user_service.update_user_password(
        id=current_user.id, hashed_password=security.get_password_hash(user.new_password))

    if not result:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to update user.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/users",
             status_code=status.HTTP_201_CREATED,
             response_model=User,
             dependencies=[Depends(get_api_key_header)],
             tags=["users"])
def add_user(user: InsertUser):
    old_user = user_service.get_user_by_username(username=user.username)
    if old_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The username {old_user.username} is not available.")

    old_email = user_service.get_user_by_email(email=user.email)
    if old_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The email {old_email.email} is not available.")

    if not is_valid_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not valid.")

    add_user = UserSchema(
        full_name=user.full_name,
        email=user.email,
        username=user.username,
        hashed_password=security.get_password_hash(user.password),
        disabled=False)

    user_service.add_user(add_user)
    new_user = user_service.get_user_by_username(username=user.username)

    return User(
        id=new_user.id,
        full_name=new_user.full_name,
        username=new_user.username,
        email=new_user.email
    )
