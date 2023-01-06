from fastapi import Depends
from .users import UserService
from api.db import get_session


def get_user_service(session=Depends(get_session)):
    return UserService(session)
