from fastapi import Depends, HTTPException, status
from api.utils import oauth2_scheme, ALGORITHM
from jose import JWTError, jwt
from api.config import get_settings
from api.services import get_user_service, UserService

settings = get_settings()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        user = user_service.get_by_username(username)
    except HTTPException:
        raise credentials_exception
    return user
