from fastapi import FastAPI
from model.config.database import engine, Base

app = FastAPI(title="OOPLAB")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"data": "Приложение успешно подключено к бд"}
