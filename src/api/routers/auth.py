from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from api.utils import authenticate_user, create_access_token
from api.services import get_user_service, UserService
from api.config import get_settings
from api.db.schemas.tokens import Token
from api.db.schemas.users import User, UserRegister
from datetime import timedelta
settings = get_settings()
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), user_service=Depends(get_user_service)):
    user = authenticate_user(
        user_service, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expires_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.post("/register", response_model=User, status_code=201)
async def register_user(user_data: UserRegister, user_service: UserService = Depends(get_user_service)):
    return user_service.create(user_data)
