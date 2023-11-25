from datetime import datetime

from fastapi import FastAPI, Response, Path, Query, Body, Header, status, Depends, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from public.users import users_router, info_router
from public.goods import good_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
"http://localhost",
"https://localhost:8080",
"http://localhost",
"http://localhost:8080",
"http://www.yandex.ru"
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,  allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = datetime.now() # начало работы метода
    response = await call_next(request) # передача запроса соответствующему оператру пути и ожидание ответа
    end_time = datetime.now() # кончание работы метода
    response.headers["X-Process-Time"] = f'{end_time} : {start_time}'
    return response
@app.get('/')
def f_indexH():
    content = {"FIO": "Половикова Ольга Николаевна"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)

@app.get("/items/", response_class=JSONResponse)
async def read_items(token: str = Depends(oauth2_scheme)):
    return JSONResponse(content={"token": token})


app.include_router(users_router)
app.include_router(info_router)
app.include_router(good_router)

@app.get('/header', response_class=JSONResponse)
def root(user_agent: str = Header(), host: str = Header(), sec_ch_ua_platform: str = Header()):
    return JSONResponse(content={"user_agent": user_agent, "host": host, "sec_ch_ua_platform": sec_ch_ua_platform})

@app.get('/find', status_code=405)
def notfind():
    return {"message": "Нет такого ресурса"}

# if __name__ == "__main__":
#     cert_file = "/path/to/cert.pem"
#     key_file = "/path/to/key.pem"
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, ssl-keyfile=key_file, ssl-certfile=cert_file)
