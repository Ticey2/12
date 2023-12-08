from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean
from config import settings

engine = create_engine(settings.POSTGRES_URL,
                       client_encoding='utf8')

from sqlalchemy.orm import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String)

Base.metadata.create_all(engine)