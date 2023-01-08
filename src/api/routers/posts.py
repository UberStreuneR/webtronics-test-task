from fastapi import APIRouter, Depends, Response
from api.router_utils import get_current_user
from api.services import get_post_service, PostService
from api.config import get_settings
from api.db.schemas.posts import Post, PostAdd, PostUpdate
from typing import List

settings = get_settings()
posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.get("/liked")
async def list_liked_posts(posts_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    return posts_service.liked_by(user.user_id)


@posts_router.post("/like/{id}")
async def like_post(id: int, posts_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    posts_service.like(id, user.user_id)
    return Response(status_code=200)


@posts_router.get("/disliked")
async def list_disliked_posts(posts_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    return posts_service.disliked_by(user.user_id)


@posts_router.post("/dislike/{id}")
async def dislike_post(id: int, posts_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    posts_service.dislike(id, user.user_id)
    return Response(status_code=200)


@posts_router.get("/", response_model=List[Post])
async def list_posts(posts_service: PostService = Depends(get_post_service)):
    return posts_service.list()


@posts_router.get("/{id}", response_model=Post)
async def get_post(id: int, posts_service: PostService = Depends(get_post_service)):
    return posts_service.get(id)


@posts_router.post("/", response_model=Post)
async def add_post(post_data: PostAdd, posts_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    return posts_service.create(post_data, user.user_id)


@posts_router.patch("/{id}", response_model=Post)
async def update_post(id: int, post_data: PostUpdate, posts_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    return posts_service.update(id, post_data, user.user_id)


@posts_router.delete("/{id}", status_code=204)
async def delete_post(id: int, posts_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    posts_service.delete(id, user.user_id)
    return Response(status_code=204)
