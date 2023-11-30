import uuid
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from models.good import Main_User, Main_UserDB, New_Respons, Tags, Good
import hashlib
from typing import Union, Annotated
from fastapi.encoders import jsonable_encoder
import models.good
import public.db as DB

# реализация маршрутов для операций c конкретными тегами - конкретизация роутера
users_router = APIRouter(tags=[Tags.users], prefix='/api/users')
info_router = APIRouter(tags=[Tags.info])

def coder_passwd(cod: str):
    result = cod*2

# Наша примитивна база данных
#users_list = [Main_UserDB(name='Ivanov', id=108, password= '**********'), Main_UserDB(name="Petrov", id=134, password="**********")]
#user_dict = {}

# для поиска пользователя в списке

@users_router.get("/api/users/{id}", response_model=Union[New_Respons, Main_User], tags=[Tags.info])
def get_user_(id: int, response: Response):
    '''
    получаем пользователя по id
    '''
    user = DB.query(Main_User).filter(Main_User.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, отправляем его
    else:
        return user
@users_router.get("/api/users", response_model=Union[list[Main_User], New_Respons], tags=[Tags.users])
def get_user_db():
    '''
    получаем все записи таблицы
    '''
    users = DB.query(Main_User).all()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if users == None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return users
@users_router.post("/api/users", response_model=Union[Main_User, New_Respons], tags=[Tags.users], status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")]):
    user = Main_UserDB(name=item.name, id=item.id, password=coder_passwd(item.name))
    #query = (models.users.insert(user))
    #record_id = await DB.database.execute(query=query)
    DB.add(user)
    DB.commit()
    DB.refresh(user)
    return user

@users_router.put("/api/users", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_person(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные для пользователя по id")]):
    # получаем пользователя по id
    user = DB.query(Main_User).filter(Main_User.id == item["id"]).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    user.name = item['name']
    DB.commit()  # сохраняем изменения
    DB.refresh(user)
    return user

@users_router.delete("/api/users/{id}", response_model=Union[list[Main_User], None], tags=[Tags.users])
def delete_person(id: int):
    # получаем пользователя по id
    user = DB.query(Main_User).filter(Main_User.id == id).first()

    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

    # если пользователь найден, удаляем его
    DB.delete(user)  # удаляем объект
    DB.commit()  # сохраняем изменения
    return user
