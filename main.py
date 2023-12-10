import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from public.router_users import init_db
from public.router_users import users_router

from config import settings
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(users_router)
@app.on_event("startup")
def on_startup():
    open("log_p.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
    init_db()

@app.on_event("shutdown")
def shutdown():
    open("log_p.txt", mode="a").write(f'{datetime.utcnow()}: End\n')
# @app.on_event("shutdown")
# async def shutdown():
#     await DB.disconnect()
#     with open("log.txt", mode="a") as log:
#         log.write(f'{datetime.utcnow()}:End\n')
@app.get("/")
def main():
    return FileResponse("files/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)