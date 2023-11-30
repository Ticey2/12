import sqlalchemy
from sqlalchemy import create_engine, MetaData
import databases
from sqlalchemy.orm import sessionmaker, declarative_base
#from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///test02.db'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


DATABASE_URL1 = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
engine = create_engine("mysql://u:p@host/db", pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
