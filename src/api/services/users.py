from sqlalchemy.orm import Session
import sqlalchemy
from api.db.models import User
from api.db.schemas.users import UserRegister
from api.utils import get_password_hash
from starlette.exceptions import HTTPException
from fastapi import status
from typing import Optional


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int) -> Optional[User]:
        user_obj = self.session.query(User).get(id)
        if user_obj is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user_obj

    def get_by_username(self, name: str) -> Optional[User]:
        user_obj = self.session.query(User).filter(
            User.username == name).first()
        if user_obj is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user_obj

    def create(self, user_data: UserRegister) -> Optional[User]:
        if user_data.password1 != user_data.password2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")
        user_obj = User(username=user_data.username,
                        hashed_password=get_password_hash(user_data.password1))
        self.session.add(user_obj)
        try:
            self.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(
                    status_code=409, detail="Username already exists")
            else:
                raise e
        return user_obj
