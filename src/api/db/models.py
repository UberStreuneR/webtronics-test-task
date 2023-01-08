from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy as sa
Base = declarative_base()


class MarkedByUser(Base):
    __tablename__ = "marked_by_user"
    user_id = sa.Column(sa.ForeignKey("users.user_id"), primary_key=True)
    post_id = sa.Column(sa.ForeignKey("posts.post_id"), primary_key=True)
    user = relationship("User", back_populates="marked_posts")
    post = relationship("Post", back_populates="marked_by")
    liked = sa.Column(sa.Boolean, nullable=False, default=True)


class User(Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, autoincrement=True,
                        nullable=False, primary_key=True)
    username = sa.Column(sa.String(15), nullable=False, unique=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    marked_posts = relationship(
        "MarkedByUser", back_populates="user", cascade="delete")


class Post(Base):
    __tablename__ = "posts"
    post_id = sa.Column(sa.Integer, autoincrement=True,
                        nullable=False, primary_key=True)
    title = sa.Column(sa.String(50), nullable=False)
    body = sa.Column(sa.Text, nullable=False)
    author_id = sa.Column(sa.ForeignKey("users.user_id"), nullable=False)
    author = relationship("User", uselist=False)
    marked_by = relationship(
        "MarkedByUser", back_populates="post", cascade="delete")
