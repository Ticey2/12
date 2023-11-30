import uvicorn
import databases
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import public.db as DB
import aiosqlite
from sqlalchemy.orm import relationship


app = FastAPI()

@app.on_event("startup")
async def startup():
    await DB.database.connect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}: Начало работы\n')

@app.on_event("shutdown")
async def shutdown():
    await DB.database.disconnect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}:Завершение работы\n')


# определяем зависимость
def get_db():
    DB = databases.SessionLocal()
    try:
        yield DB
    finally:
        DB.close()


@app.get("/")
def main():
    return FileResponse("/OLD/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)