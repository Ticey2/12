from config import settings
from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy import create_engine, text
from models.good import Base
from sqlalchemy.orm import declarative_base

# определяем параметры для подключения

# settings.DATABASE_URL = 'sqlite:///./test02.db
# engine = create_engine(settings.POSTGRES_DATABASE_URL)

#ur_p = "postgresql://postgres:900@localhost:5432/dbtest04"

ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA

print(ur_s)

engine_s = create_engine(ur_s, echo=True)
# engine_a = create_async_engine(ur_a, echo=True)


def create_tables():
    #Base.metadata.drop_all(bind=engine_s)
    Base.metadata.create_all(bind=engine_s)
    # metadata.create_all(bind=engine_s)


def f():
    with engine_s.connect() as conn:
        answer = conn.execute(text("select version()"))
        print(f"answer = {answer.all()}")

# asyncio.run(f())
# asyncio.get_event_loop().run_until_complete(f())
