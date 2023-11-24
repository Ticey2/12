from typing import Optional, Union
from fastapi import Depends, FastAPI, Header, HTTPException,


def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# async def get_db():
#     db = DBSession() # не подключили нужные библиотеки ещё
#     try:
#         yield db
#     finally:
#         db.close()


app = FastAPI(dependencies = [Depends(verify_token)])

@app.get("/items/")
def read_items(obj = Depends(get_db())):
    return obj

class Read_Params:
    def __init__(self, params: Union[str, None] = None, skip: int = 0, limit: int= 100):
        self. params = params
        self.skip = skip
        self. limit = limit


@app.get("/users/")
def read_users(obj: Read_Params = Depends(Read_Params)):
    return obj