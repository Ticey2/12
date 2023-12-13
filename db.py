#from fastapi import APIRouter, Body, status, HTTPException, Depends
#from fastapi.responses import JSONResponse, Response
#from sqlalchemy.orm import sessionmaker, declarative_base, Session
#from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
#from models.good import Main_User, New_Respons, Tags, User, Base
#import psycopg
from sqlalchemy import create_engine, text
# определяем параметры для подключения

#settings.DATABASE_URL = 'sqlite:///./test02.db

#engine = create_engine(settings.POSTGRES_DATABASE_URL)
ur_p = "postgresql://postgres:900@localhost:5432/dbtest04"

engine = create_engine(ur_p, echo=True)
#SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

with engine.connect() as conn:
    res = conn.execute(text("select version()"))
    print(f"res = {res.all()}")