from typing import List
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = "new_users"
    id: Mapped[int]
    name: Mapped[str]
    hashedpassword: Mapped[Optional[str]]
class Address(Base):
    __tablename__ = "goods"
    id: Mapped[int]
    email_address: Mapped[str]
    user_id: Mapped[int] = relationship(back_populates="new_users")
