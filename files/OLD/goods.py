from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import Response
from models.good import New_Respons, Tags, Good
from typing import Union, Annotated
from fastapi.encoders import jsonable_encoder


good_router = APIRouter(tags=[Tags.good])

good_dict = {}

def find_good(id: str) -> Union[Good, None]:
    if good_dict.get(id):
        return good_dict[id]
    else:
        return None
@good_router.get("/api/goods", response_model=Union[dict, New_Respons], tags=[Tags.good])
def get_good_dict():
    '''
    получаем все записи словаря-базы
    '''
    return good_dict

@good_router.post("/api/goods", response_model=Union[dict, New_Respons], tags=[Tags.good])
def create_good(item: Good):
    good_encoder = jsonable_encoder(item)
    good_dict[str(item.id)] = good_encoder
    return good_encoder


@good_router.put("/api/goods", response_model=Union[dict, New_Respons], tags=[Tags.good])
def edit_good_up(item: Annotated[Good, Body(embed=True, description="Изменяем данные товара по id")]):
    # получаем пользователя по id
    good_encoder = jsonable_encoder(item)
    good_dict[str(item.id)] = good_encoder
    return good_dict

@good_router.patch("/api/goods", response_model=Union[Good, New_Respons], tags=[Tags.good])
def edit_good(item: Annotated[Good, Body(embed=True, description="Изменяем данные товара по id")], response: Response):
    # получаем пользователя по id
    try:
        item_good = find_good(str(item.id)) #нашли элемент по ключу
        # item_good = good_dict[str(item.id)]
        if item_good == None:
            return New_Respons(message="ошибка")

        good_model = Good(**item_good)   #преобразовали элемент из словаря в модель

        update_good_dict = item.dict(exclude_unset=True) #преобразуем объект модели в словарь, но только только те данные,
        # которые были установлены (отправлены в запросе), без значений по умолчанию (данные для изменения в удобный
        # формат)
        good_model_copy = good_model.copy(update=update_good_dict) # обновляем данные  модели на новые
        good_dict[str(item.id)] = jsonable_encoder(good_model_copy)
        return good_model_copy
    except HTTPException:
        return New_Respons(message = f'Ошибка {response.status_code}')

