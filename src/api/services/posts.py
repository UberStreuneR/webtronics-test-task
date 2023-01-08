from sqlalchemy.orm import Session, Query
import sqlalchemy
from api.db.models import Post, MarkedByUser
from api.db.schemas.posts import PostAdd, PostUpdate
from starlette.exceptions import HTTPException

from typing import Optional, List, Tuple


class PostService:
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int) -> Optional[Post]:
        post_obj = self.session.query(Post).get(id)
        if post_obj is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post_obj

    def list(self) -> List[Post]:
        return self.session.query(Post).all()

    def create(self, post_data: PostAdd, author_id: int) -> Optional[Post]:
        post_obj = Post(**post_data.dict(), author_id=author_id)
        self.session.add(post_obj)
        try:
            self.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            elif "is not present" in str(e):
                raise HTTPException(
                    status_code=400, detail="No user with such id")
            raise e
        return post_obj

    def update(self, id: int, post_data: PostUpdate, user_id: int) -> Optional[Post]:
        post_obj = self.get(id)
        if not self.check_posts_author(post_obj, user_id):
            raise HTTPException(
                status_code=400, detail="Cannot update other users' posts")
        for column, value in post_data.dict(exclude_unset=True).items():
            setattr(post_obj, column, value)
        self.session.commit()
        return post_obj

    def delete(self, id: int, user_id: int) -> None:
        post_obj = self.get(id)
        if not self.check_posts_author(post_obj, user_id):
            raise HTTPException(
                status_code=400, detail="Cannot delete other users' posts")
        self.session.delete(post_obj)
        self.session.commit()

    def get_or_create_assoc(self, id: int, user_id: int, liked=True) -> Tuple[MarkedByUser, bool]:
        post_obj = self.get(id)
        if self.check_posts_author(post_obj, user_id):
            raise HTTPException(
                status_code=400, detail="Cannot like or dislike one's own posts")
        assoc_obj = self.session.query(MarkedByUser).filter(
            MarkedByUser.user_id == user_id, MarkedByUser.post_id == post_obj.post_id).first()
        created = False
        if assoc_obj is None:
            assoc_obj = MarkedByUser(
                user_id=user_id, post_id=post_obj.post_id, liked=liked)
            created = True
            self.session.add(assoc_obj)
            self.session.commit()
        print(assoc_obj, created)
        return assoc_obj, created

    def like(self, id: int, user_id: int) -> None:
        assoc_obj, created = self.get_or_create_assoc(id, user_id)
        if not created:
            if not assoc_obj.liked:
                assoc_obj.liked = True
            else:
                self.session.delete(assoc_obj)
        self.session.commit()

    def dislike(self, id: int, user_id: int) -> None:
        assoc_obj, created = self.get_or_create_assoc(id, user_id, liked=False)
        if not created:
            if not assoc_obj.liked:
                self.session.delete(assoc_obj)
            else:
                assoc_obj.liked = False
        self.session.commit()

    def get_posts_marked_by(self, user_id: int) -> Query:
        posts = self.session.query(Post).join(MarkedByUser).filter(MarkedByUser.user_id == user_id).filter(
            MarkedByUser.post_id == Post.post_id
        )
        return posts

    def liked_by(self, user_id: int) -> List[Post]:
        posts = self.get_posts_marked_by(user_id)
        return posts.filter(MarkedByUser.liked == True).all()

    def disliked_by(self, user_id: int) -> List[Post]:
        posts = self.get_posts_marked_by(user_id)
        return posts.filter(MarkedByUser.liked == False).all()

    def check_posts_author(self, post_obj: Post, user_id: int) -> bool:
        if post_obj.author_id == user_id:
            return True
        return False
