
from sqlalchemy import create_engine
from fastapi import APIRouter, Body, status,HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from models.good import Main_User, New_Respons, Tags, User, Base

from typing import Union, Annotated


# определяем параметры для подключения

DATABASE_URL = 'sqlite:///./test02.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        try:
          yield session
        finally:
          session.close()

# реализация маршрутов для операций c конкретными тегами - конкретизация роутера
users_router = APIRouter(tags=[Tags.users], prefix='/api/users')
info_router = APIRouter(tags=[Tags.info])
def coder_passwd(cod: str):
    return cod*2
# Наша примитивная база данных
#users_list = [Main_UserDB(name='Ivanov', id=108, password= '**********'), Main_UserDB(name="Petrov", id=134, password="**********")]
#user_dict = {}
@users_router.get("/{id}", response_model=Union[New_Respons, Main_User], tags=[Tags.info])
def get_user_(id: int, response: Response, DB: Session = Depends(get_session)):
    '''
    получаем пользователя по id
    '''
    user = DB.query(User).filter(User.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, отправляем его
    else:
        return user
@users_router.get("/", response_model=Union[list[Main_User], New_Respons], tags=[Tags.users])
def get_user_db(DB: Session = Depends(get_session) ):
    '''
    получаем все записи таблицы
    '''
    users = DB.query(User).all()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if users == None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return users
@users_router.post("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users], status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")],  DB: Session = Depends(get_session)):
    try:
      user = User(id=item.id, name=item.name, hashed_password=item.name)

      if user is None:
          raise HTTPException(status_code=404, detail="Объект не определен")
      DB.add(user)
      DB.commit()
      DB.refresh(user)
      return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {user}")


@users_router.put("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_person(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные для пользователя по id")], DB: Session = Depends(get_session)):
    # получаем пользователя по id
    user = DB.query(User).filter(User.id == item.id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    user.name = item['name']
    DB.commit()  # сохраняем изменения
    DB.refresh(user)
    return user

@users_router.delete("/{id}", response_model=Union[list[Main_User], None], tags=[Tags.users])
def delete_person(id: int, DB: Session = Depends(get_session)):
    # получаем пользователя по id
    user = DB.query(User).filter(User.id == id).first()

    # если не найден, отправляем статусный код и сообщение об ошибке
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

    # если пользователь найден, удаляем его
    DB.commit()  # сохраняем изменения
    return user
