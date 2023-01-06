from fastapi import APIRouter, Depends
from api.config import get_settings
from api.db.schemas.users import User
from api.router_utils import get_current_user
settings = get_settings()
users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=User)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
