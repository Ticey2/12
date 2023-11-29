import uvicorn
import databases
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import aiosqlite
from sqlalchemy.orm import relationship

DATABASE_URL = 'sqlite:///test02.db'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}: Начало работы\n')

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}:Завершение работы\n')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)