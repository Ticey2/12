import uuid
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from models.good import Main_User, Main_UserDB, New_Respons, Tags, Good
import hashlib
from typing import Union, Annotated
from fastapi.encoders import jsonable_encoder
from main import

# реализация маршрутов для операций c конкретными тегами - конкретизация роутера
users_router = APIRouter(tags=[Tags.users])
info_router = APIRouter(tags=[Tags.info])
def coder_passwd(cod: str):
    result = cod*2


# Наша примитивна база данных
users_list = [Main_UserDB(name='Ivanov', id=108, password= '**********'), Main_UserDB(name="Petrov", id=134, password="**********")]
user_dict = {}


# для поиска пользователя в списке
def find_user(id: int) -> Union[Main_UserDB, None]:
    for user in users_list:
        if user.id == id:
            return user
    return None

@users_router.get("/api/users", response_model=Union[list[Main_User], None], tags=[Tags.users], summary="Операция для")
def get_users():
    '''
    Класс APIRouter принадлежит пакету FastAPI и создает операции пути для
    нескольких маршрутов. Класс APIRouter предназначен для модульности и организации
    маршрутизации.
    Класс APIRouter работает так же, как и класс FastAPI. Однако uvicorn не может
    использовать экземпляр APIRouter для обслуживания приложения, в отличие
    от FastAPIs.
    Маршруты, определенные с помощью класса APIRouter, должны быть добавлены в
    к объекту fastapi для обеспечения их видимости.
    '''
    from fastapi.encoders import jsonable_encoder
    return users_list


@users_router.get("/api/users/{id}", response_model=Union[New_Respons, Main_User], tags=[Tags.users])
def get_user(id: int, response: Response):
    '''
    получаем пользователя по id
    '''
    try:
      user = find_user(id)

      return user
    except HTTPException:
      return New_Respons(message = "Пользователь не найден")
@info_router.get("/api/users/{id}-{id1}", response_model=Union[New_Respons, Main_User], tags=[Tags.info])
def get_user_(id: int, id1: int, response: Response):
    '''
    получаем пользователя по id
    '''
    user = find_user(id)
    print(user)
    # если не найден, отправляем сообщение об ошибке
    if user == None:
        response.status_code = 404
        return New_Respons(message="Пользователь не найден")
    # если пользователь найден, отправляем его
    else:
        return user
@users_router.get("/api/users_dict", response_model=Union[dict, New_Respons], tags=[Tags.users])
def get_user_dict():
    '''
    получаем все записи словаря-базы
    '''
    return user_dict
@users_router.post("/api/users", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")]):

    user = Main_UserDB(name=item.name, id=item.id, password=coder_passwd(item.name))
    query = ( users.insert().values(title=post.title, description=post.description, completed=False)
    )
    # добавляем объект в список
    users_list.append(user)

    # добавляем объект в словарь
    user_encoder = jsonable_encoder(user)
    user_dict[str(item.id)] = user_encoder
    return user_encoder

@app.post("/set_task", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(post: TaskSet):

    last_record_id = await database.execute(query=query)
    return {"id": last_record_id, **post.model_dump(), "completed": False}

@users_router.put("/api/users", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_person(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные для пользователя по id")]):
    # получаем пользователя по id
    user = find_user(item.id)
    # если не найден
    if user == None:
        return New_Respons(message= "Пользователь не найден")
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    #user.id = item.id
    user.name = item.name
    return user

@users_router.delete("/api/users/{id}", response_model=Union[list[Main_User], None], tags=[Tags.users])
def delete_person(id: int):
    # получаем пользователя по id
    user = find_user(id)

    # если не найден
    if user == None:
        return New_Respons(message= "Пользователь не найден")

    # если пользователь найден, удаляем его
    users_list.remove(user)
    return users_list


@app.post("/set_task", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(post: TaskSet):
    query = (
        tasks.insert()
        .values(title=post.title, description=post.description, completed=False)
    )
    last_record_id = await database.execute(query=query)
    return {"id": last_record_id, **post.model_dump(), "completed": False}

@app.get('/read_task/{task_id}', response_model=Task)
async def read_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    if res := await database.fetch_one(query=query):
        return res
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Task with id:{task_id} not found'
    )

@app.post('/update_task', response_model=Task)
async def update_task(post: Task):
    query = (
        tasks.update()
        .where(tasks.c.id == post.id)
        .values(title=post.title, description=post.description, completed=post.completed)
    )
    if await database.execute(query=query):
        return {**post.model_dump()}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Task with id:{post.id} not found'
    )

@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    if await database.execute(query):
        return {"detail": f'Task with id: {task_id} deleted'}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Task with id:{task_id} not found'
    )
