from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def f_index():
    return {"message": "World___", "keyroot": "Привет!"}


@app.get('/tools')
async def f_indexT():
    return "Good day!"
