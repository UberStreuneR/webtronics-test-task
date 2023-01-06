from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, autoincrement=True,
                        nullable=False, primary_key=True)
    username = sa.Column(sa.String(15), nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
