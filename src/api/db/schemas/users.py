from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str

    class Config:
        orm_mode = True


class UserInDB(User):
    password: str


class UserRegister(BaseModel):
    username: str
    password1: str
    password2: str
