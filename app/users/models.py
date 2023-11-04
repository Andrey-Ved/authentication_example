from sqlalchemy import Column, Integer, String

from app.core.db_base import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __str__(self):
        return f"User {self.email}"


print('init users models')
