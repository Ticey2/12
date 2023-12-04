from fastapi import FastAPI, Path, Query, Body, Header
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, FileResponse
from models.good import Good
from models.good import User
from models.good import Person
from typing import Union, Annotated

app = FastAPI()

@app.on_event("startup")
async def startup():
    await DB.connect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}: Begin\n')

@app.on_event("shutdown")
async def shutdown():
    await DB.disconnect()
    with open("log.txt", mode="a") as log:
        log.write(f'{datetime.utcnow()}:End\n')

# аннотирование параметров
@app.get("/params/{p}")
async def read_params(p: Annotated[int, Path(description='int' , title = "good params")], q: Annotated[Union[str, None],
                      Query(description="Специальный параметр для ...",
                      min_length=3, max_length=30)] = None):
    results = {"results": p}
    if q:
        results.update({"q": q})
    return results

@app.get("/params1/{p}")
async def read_params(p: Annotated[int, Path(description='int')],
                    param_person: Union[Person, None]= None,  param_person1: Union[Person, None]= None):
    results = {"results": p}
   # if param_user:
   #     results.update({"user": param_user.dict()})
    if param_person:
        results.update({"person": param_person.dict()})
    return results

@app.get("/params2/{p}")
async def read_params(p: Annotated[int, Path(description='int')],
                      user_id: Annotated[int, Body(description="kgfldkg")] = 0):
    results = {"results": p}
   # if param_user:
   #     results.update({"user": param_user.dict()})
    if user_id:
        results.update({"user_id": user_id})

@app.post('/user/', response_class=JSONResponse)
def create_user(obj: Union[User, None] = None):
    if obj is not None:
        return {'obj': obj}
    else:
        return {'obj': "--"}

@app.post('/good/', response_class=JSONResponse)
def create_obj(obj: Union[Good, None] = None):
    if obj is not None:
        return {'obj': obj}
    else:
        return {'obj': "пустой"}


@app.put("/users/{id}")
def create_user_id(id: int, user: User, s: Union[str, None] = None):
    result = {"id_": id, **user.dict()}
    if s is not None:
        result.update({"s": s})
    return result


@app.post('/goods/', response_class=JSONResponse)
def create_item(goods: Union[list[Good], None] = None):
    if goods is None:
        a = []
    else:
        a = [f'{x.name} : {str(x.price * (1 + x.nalog))}' for x in goods]
    return {'name_goods': ' - '.join(a)}


@app.post('/id/{id}', response_class=JSONResponse)
def create_item(id: int, goods: Union[list[Good], None] = None):
    a = [f'{x.name} : {str(x.price * (1 + x.nalog))}' for x in goods]
    return {'name_goods': a, 'id': id}


@app.post('/good_peron/', response_class=JSONResponse)
def create_item(obj1: Union[Person, None] = None):
    return {'obj': obj1}


@app.post('/params')
def root_func(name: str):
    html_content = f'<H1>{name}, Good day</H1>'
    return HTMLResponse(content=html_content)


@app.get('/users/{name}-{id}')
def read_get(name: str = Path(min_length=3, max_length=20), id: int = Path(gt=300, lt=1000)):
    html_content = f"<b>Good day, {name} ({id})</b>"
    return HTMLResponse(content=html_content)


@app.get('/forms/{name_user}')
def f_indexF(name_user: str, id: int = 100, id1: int = 345):
    return {'message': f"{name_user}, good day! id= {id} {id1}"}


@app.get('/name_user')
def f_indexF(name_user: str = 'Lena', id: int = 100, id1: int = 345):
    return {'message': f"{name_user}, good day! id= {id} {id1}"}

@app.get('/forms/new-form')
def f_indexN():
    return {'message': "good day!"}


@app.get('/html', response_class=PlainTextResponse)
def f_indexH():
    return "<b> Hello, User! </b>"


@app.get('/file')
def f_indexF():
    return FileResponse("../index.html", filename="1.html", media_type="application/octet-steam")

@app.get("/header")
async def read_header(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}

@app.get("/")
def get_headers():
    content = {"FIO": "Половикова Ольга Николаевна"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)



