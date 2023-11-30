from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from models import tables
from public.db import engine, database

app = FastAPI()

tables.Base.metadata.create_all(bind=engine)
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
def f_indexH():
    content = {"FIO": "Половикова Ольга Николаевна"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)

@app.get('/header', response_class=JSONResponse)
def root(user_agent: str = Header(), host: str = Header(), sec_ch_ua_platform: str = Header()):
    return JSONResponse(content={"user_agent": user_agent, "host": host, "sec_ch_ua_platform": sec_ch_ua_platform})


# if __name__ == "__main__":
#     cert_file = "/path/to/cert.pem"
#     key_file = "/path/to/key.pem"
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, ssl-keyfile=key_file, ssl-certfile=cert_file)
